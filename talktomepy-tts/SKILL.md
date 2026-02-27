---
name: talktomepy-tts
description: Use this skill when the user wants text read aloud using the local TalkToMePy v0.5+ TTS HTTP service in VoiceDesign mode. It generates WAV audio via /synthesize/voice-design, saves it in the current workspace, and plays it on macOS with afplay.
---

# TalkToMePy TTS

Use this skill when the user asks to hear text spoken aloud from the local machine.

## What this skill does

- Calls the local TalkToMePy v0.5+ service (`/health`, `/model/load`, `/model/status`, `/synthesize/voice-design`)
- Handles async model loading behavior (`/model/load` may return `202`)
- Retries synthesis on `503` using `Retry-After`
- Saves generated WAV output to `./tts_outputs` in the current working directory by default
- Plays audio via `afplay` on macOS

## Preconditions

- TalkToMePy service is running (default `http://127.0.0.1:8000`)
- macOS `afplay` is available

## Default workflow

1. Ensure service is healthy:
   - `curl -fsS http://127.0.0.1:8000/health`
2. Trigger model load (idempotent):
   - `curl -sS -X POST http://127.0.0.1:8000/model/load -H "Content-Type: application/json" -d '{"mode":"voice_design","strict_load":false}'`
3. Wait for ready state via `/model/status`
4. Synthesize + save + play using bundled script:
   - `scripts/speak_with_talktomepy.sh --text "..."`

## Script usage

```bash
scripts/speak_with_talktomepy.sh --text "Read this text aloud"
```

Defaults:

- `language`: `English`
- default style: `energetic` (warm/friendly/brisk feminine-or-androgynous)
- output path: `./tts_outputs/tts-YYYYMMDD-HHMMSS.wav`

Style preset flags:

- `--style-energetic`
- `--style-soft`
- `--style-neutral`

Alternative style syntax:

- `--style energetic|soft|neutral`

Optional flags:

- `--instruct "..."` fully custom voice/style instruction
- `--language English`
- `--base-url http://127.0.0.1:8000`
- `--save /path/output.wav` custom save path
- `--no-play` generate only, do not play

Optional env var overrides:

- `TALKTOMEPY_BASE_URL`
- `TALKTOMEPY_OUTPUT_DIR`
- `TALKTOMEPY_MAX_WAIT_SECONDS`
- `TALKTOMEPY_MAX_SYNTH_RETRIES`
- `TALKTOMEPY_DEFAULT_RETRY_AFTER_SECONDS`

If synthesis fails, surface HTTP status/body and suggest checking:
- `/model/status`
- launchd logs: `~/Library/Logs/talktomepy.stderr.log`
