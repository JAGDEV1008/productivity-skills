#!/usr/bin/env python3
"""Read-only cleanup audit for repositories under a workspace root."""

from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

DIR_RULES: Dict[str, Tuple[str, int]] = {
    "dist": ("build_output", 10),
    "build": ("build_output", 10),
    ".next": ("build_output", 10),
    ".nuxt": ("build_output", 10),
    ".turbo": ("build_output", 8),
    "target": ("build_output", 10),
    "out": ("build_output", 8),
    "node_modules": ("dependency_artifact", 16),
    ".venv": ("dependency_artifact", 14),
    "venv": ("dependency_artifact", 14),
    ".gradle": ("dependency_artifact", 16),
    ".m2": ("dependency_artifact", 12),
    ".cache": ("tool_cache", 8),
    ".parcel-cache": ("tool_cache", 8),
    ".ruff_cache": ("tool_cache", 6),
    ".mypy_cache": ("tool_cache", 6),
    ".pytest_cache": ("tool_cache", 6),
    "__pycache__": ("tool_cache", 5),
}

FILE_EXT_RULES: Dict[str, Tuple[str, int]] = {
    ".log": ("transient_file", 12),
    ".tmp": ("transient_file", 10),
    ".temp": ("transient_file", 10),
    ".cache": ("transient_file", 10),
    ".zip": ("archive", 10),
    ".tar": ("archive", 10),
    ".tgz": ("archive", 10),
    ".gz": ("archive", 8),
    ".bz2": ("archive", 8),
    ".xz": ("archive", 8),
}

GIB = 1024**3
MIB = 1024**2


@dataclass
class Finding:
    severity: str
    score: int
    repo: str
    directory: str
    category: str
    size_bytes: int
    size_human: str
    why_flagged: str
    suggested_cleanup: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan repositories in a workspace for cleanup chores (read-only)."
    )
    parser.add_argument(
        "--workspace",
        default="~/Workspace",
        help="Workspace root containing repositories (default: ~/Workspace)",
    )
    parser.add_argument(
        "--min-mb",
        type=float,
        default=50.0,
        help="Ignore findings smaller than this size in MiB (default: 50)",
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=90,
        help="Boost score when artifacts are older than this many days (default: 90)",
    )
    parser.add_argument(
        "--max-findings",
        type=int,
        default=200,
        help="Maximum findings to include in output (default: 200)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON output instead of text report",
    )
    return parser.parse_args()


def human_bytes(num_bytes: int) -> str:
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    value = float(num_bytes)
    unit = units[0]
    for unit in units:
        if value < 1024.0 or unit == units[-1]:
            break
        value /= 1024.0
    if unit == "B":
        return f"{int(value)} {unit}"
    return f"{value:.1f} {unit}"


def find_repositories(workspace_root: Path) -> List[Path]:
    repos: List[Path] = []
    for root, dirs, _ in os.walk(workspace_root, topdown=True):
        root_path = Path(root)
        if ".git" in dirs or (root_path / ".git").is_file():
            repos.append(root_path)
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if d not in {".git", ".svn", ".hg"}]
    return sorted(set(repos))


def dir_size_and_latest_mtime(path: Path) -> Tuple[int, float]:
    total = 0
    latest = path.stat().st_mtime if path.exists() else 0.0
    for root, dirs, files in os.walk(path, topdown=True, followlinks=False):
        dirs[:] = [d for d in dirs if d not in {".git"}]
        for filename in files:
            file_path = Path(root) / filename
            try:
                stat_result = file_path.stat()
            except OSError:
                continue
            total += stat_result.st_size
            if stat_result.st_mtime > latest:
                latest = stat_result.st_mtime
    return total, latest


def file_rule_for(path: Path) -> Tuple[str, int] | None:
    suffix = path.suffix.lower()
    if suffix in FILE_EXT_RULES:
        return FILE_EXT_RULES[suffix]
    return None


def base_size_score(size_bytes: int) -> int:
    if size_bytes >= 5 * GIB:
        return 84
    if size_bytes >= 2 * GIB:
        return 72
    if size_bytes >= 1 * GIB:
        return 60
    if size_bytes >= 200 * MIB:
        return 42
    return 26


def severity_from_score(score: int) -> str:
    if score >= 85:
        return "critical"
    if score >= 70:
        return "high"
    if score >= 45:
        return "medium"
    return "low"


def sorted_findings(findings: Iterable[Finding]) -> List[Finding]:
    severity_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return sorted(
        findings,
        key=lambda f: (severity_rank[f.severity], -f.score, -f.size_bytes, f.repo, f.directory),
    )


def scan_repo(repo: Path, min_bytes: int, stale_days: int, now_ts: float) -> List[Finding]:
    findings: List[Finding] = []

    for root, dirs, files in os.walk(repo, topdown=True, followlinks=False):
        root_path = Path(root)

        for dirname in list(dirs):
            rule = DIR_RULES.get(dirname)
            if not rule:
                continue

            candidate = root_path / dirname
            size_bytes, latest_mtime = dir_size_and_latest_mtime(candidate)
            dirs.remove(dirname)
            if size_bytes < min_bytes:
                continue

            category, weight = rule
            score = base_size_score(size_bytes) + weight + age_bonus_with_now(latest_mtime, stale_days, now_ts)
            score = min(100, score)
            severity = severity_from_score(score)
            findings.append(
                Finding(
                    severity=severity,
                    score=score,
                    repo=str(repo),
                    directory=str(candidate),
                    category=category,
                    size_bytes=size_bytes,
                    size_human=human_bytes(size_bytes),
                    why_flagged=(
                        f"Matched directory pattern '{dirname}' with {human_bytes(size_bytes)} of removable artifacts."
                    ),
                    suggested_cleanup=(
                        "Review and remove/rebuild this artifact directory if not needed for active work."
                    ),
                )
            )

        for filename in files:
            candidate_file = root_path / filename
            rule = file_rule_for(candidate_file)
            if not rule:
                continue
            try:
                stat_result = candidate_file.stat()
            except OSError:
                continue
            if stat_result.st_size < min_bytes:
                continue

            category, weight = rule
            score = base_size_score(stat_result.st_size) + weight + age_bonus_with_now(
                stat_result.st_mtime, stale_days, now_ts
            )
            score = min(100, score)
            severity = severity_from_score(score)

            findings.append(
                Finding(
                    severity=severity,
                    score=score,
                    repo=str(repo),
                    directory=str(candidate_file),
                    category=category,
                    size_bytes=stat_result.st_size,
                    size_human=human_bytes(stat_result.st_size),
                    why_flagged=(
                        f"Large transient or archive file '{candidate_file.name}' at {human_bytes(stat_result.st_size)}."
                    ),
                    suggested_cleanup=(
                        "Remove or relocate if this file is not needed for current development tasks."
                    ),
                )
            )

    return findings


def age_bonus_with_now(latest_mtime: float, stale_days: int, now_ts: float) -> int:
    if latest_mtime <= 0:
        return 0
    age_seconds = max(0.0, now_ts - latest_mtime)
    age_days = age_seconds / 86400.0
    if age_days >= stale_days * 2:
        return 10
    if age_days >= stale_days:
        return 6
    if age_days >= stale_days / 2:
        return 3
    return 0


def summarize_by_repo(findings: List[Finding]) -> List[dict]:
    summary: Dict[str, dict] = {}
    for finding in findings:
        row = summary.setdefault(
            finding.repo,
            {
                "repo": finding.repo,
                "total_size_bytes": 0,
                "total_size_human": "0 B",
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "findings": 0,
            },
        )
        row["total_size_bytes"] += finding.size_bytes
        row[finding.severity] += 1
        row["findings"] += 1

    rows = list(summary.values())
    for row in rows:
        row["total_size_human"] = human_bytes(row["total_size_bytes"])

    rows.sort(key=lambda item: (-item["total_size_bytes"], -item["critical"], -item["high"], item["repo"]))
    return rows


def text_report(findings: List[Finding], repo_summary: List[dict], scanned_repo_count: int, workspace: Path) -> str:
    lines: List[str] = []
    lines.append(f"Workspace Cleanup Audit (read-only)")
    lines.append(f"Workspace: {workspace}")
    lines.append(f"Repositories scanned: {scanned_repo_count}")
    lines.append(f"Findings: {len(findings)}")
    lines.append("")

    if findings:
        lines.append("Ranked Findings")
        for idx, finding in enumerate(findings, start=1):
            lines.append(
                f"{idx}. [{finding.severity.upper()}] score={finding.score} size={finding.size_human} "
                f"category={finding.category}"
            )
            lines.append(f"   repo: {finding.repo}")
            lines.append(f"   directory: {finding.directory}")
            lines.append(f"   reason: {finding.why_flagged}")
            lines.append(f"   cleanup: {finding.suggested_cleanup}")
        lines.append("")
    else:
        lines.append("No findings above threshold.")
        lines.append("")

    lines.append("Repo Summary")
    if repo_summary:
        for row in repo_summary:
            lines.append(
                f"- {row['repo']}: {row['total_size_human']} across {row['findings']} findings "
                f"(critical={row['critical']}, high={row['high']}, medium={row['medium']}, low={row['low']})"
            )
    else:
        lines.append("- No flagged repositories.")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    if not workspace.exists() or not workspace.is_dir():
        raise SystemExit(f"Workspace path does not exist or is not a directory: {workspace}")

    min_bytes = int(args.min_mb * MIB)
    now_ts = time.time()

    repos = find_repositories(workspace)
    all_findings: List[Finding] = []
    for repo in repos:
        all_findings.extend(scan_repo(repo, min_bytes=min_bytes, stale_days=args.stale_days, now_ts=now_ts))

    ranked = sorted_findings(all_findings)[: args.max_findings]
    repo_summary = summarize_by_repo(ranked)

    payload = {
        "workspace": str(workspace),
        "scanned_repo_count": len(repos),
        "findings": [asdict(item) for item in ranked],
        "repo_summary": repo_summary,
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(text_report(ranked, repo_summary, len(repos), workspace))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
