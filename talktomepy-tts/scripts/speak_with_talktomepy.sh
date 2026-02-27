#!/bin/bash
set -euo pipefail

BASE_URL="${TALKTOMEPY_BASE_URL:-http://127.0.0.1:8000}"
TEXT=""
STYLE="energetic"
INSTRUCT="A warm, friendly, energetic, feminine-or-androgynous voice with brisk pacing, clear articulation, and natural expression."
LANGUAGE="English"
SAVE_PATH=""
PLAY_AUDIO="true"
DEFAULT_OUTPUT_DIR="${TALKTOMEPY_OUTPUT_DIR:-$PWD/tts_outputs}"
MAX_WAIT_SECONDS="${TALKTOMEPY_MAX_WAIT_SECONDS:-180}"
MAX_SYNTH_RETRIES="${TALKTOMEPY_MAX_SYNTH_RETRIES:-12}"
DEFAULT_RETRY_AFTER_SECONDS="${TALKTOMEPY_DEFAULT_RETRY_AFTER_SECONDS:-5}"

set_style() {
  case "$1" in
    energetic)
      INSTRUCT="A warm, friendly, energetic, feminine-or-androgynous voice with brisk pacing, clear articulation, and natural expression."
      ;;
    soft)
      INSTRUCT="A warm, gentle, feminine-or-androgynous voice with calm pacing, soft energy, and clear but relaxed articulation."
      ;;
    neutral)
      INSTRUCT="A clear, natural, androgynous voice with medium pace, balanced tone, and clean articulation."
      ;;
    *)
      echo "Unknown style: $1 (expected: energetic, soft, neutral)" >&2
      exit 1
      ;;
  esac
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --text)
      TEXT="${2:-}"
      shift 2
      ;;
    --instruct)
      INSTRUCT="${2:-}"
      shift 2
      ;;
    --language)
      LANGUAGE="${2:-}"
      shift 2
      ;;
    --base-url)
      BASE_URL="${2:-}"
      shift 2
      ;;
    --save)
      SAVE_PATH="${2:-}"
      shift 2
      ;;
    --style)
      STYLE="${2:-}"
      set_style "$STYLE"
      shift 2
      ;;
    --style-energetic)
      STYLE="energetic"
      set_style "$STYLE"
      shift
      ;;
    --style-soft)
      STYLE="soft"
      set_style "$STYLE"
      shift
      ;;
    --style-neutral)
      STYLE="neutral"
      set_style "$STYLE"
      shift
      ;;
    --no-play)
      PLAY_AUDIO="false"
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$TEXT" ]]; then
  echo "Missing required argument: --text" >&2
  exit 1
fi

if ! command -v curl >/dev/null 2>&1; then
  echo "curl is required" >&2
  exit 1
fi

if [[ "$PLAY_AUDIO" == "true" ]] && ! command -v afplay >/dev/null 2>&1; then
  echo "afplay is required for playback (macOS)" >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required for JSON-safe payload encoding" >&2
  exit 1
fi

json_field() {
  local json_input="$1"
  local field_name="$2"
  python3 - "$json_input" "$field_name" <<'PY'
import json
import sys
raw, field = sys.argv[1], sys.argv[2]
try:
    data = json.loads(raw)
except Exception:
    print("")
    raise SystemExit(0)
value = data.get(field, "")
if value is None:
    print("")
else:
    print(value)
PY
}

wait_for_model_ready() {
  local waited=0
  local interval=2

  while (( waited <= MAX_WAIT_SECONDS )); do
    local status_json
    status_json="$(curl -sS "$BASE_URL/model/status" || true)"

    local loaded loading ready detail
    loaded="$(json_field "$status_json" "loaded")"
    loading="$(json_field "$status_json" "loading")"
    ready="$(json_field "$status_json" "ready")"
    detail="$(json_field "$status_json" "detail")"
    if [[ "$loaded" == "True" || "$loaded" == "true" ]]; then
      return 0
    fi

    if [[ "$ready" != "True" && "$ready" != "true" ]]; then
      echo "Model runtime is not ready: $detail" >&2
      return 1
    fi

    if [[ "$loading" != "True" && "$loading" != "true" ]]; then
      # Not loaded and not loading. Try to trigger load again.
      curl -sS -X POST "$BASE_URL/model/load" \
        -H "Content-Type: application/json" \
        -d '{"mode":"voice_design","strict_load":false}' >/dev/null || true
    fi

    sleep "$interval"
    waited=$((waited + interval))
  done

  echo "Timed out waiting for model to become ready after ${MAX_WAIT_SECONDS}s" >&2
  return 1
}

curl -fsS "$BASE_URL/health" >/dev/null

LOAD_STATUS="$(curl -sS -o /tmp/talktomepy-load-response.json -w "%{http_code}" -X POST "$BASE_URL/model/load" \
  -H "Content-Type: application/json" \
  -d '{"mode":"voice_design","strict_load":false}')"
if [[ "$LOAD_STATUS" != "200" && "$LOAD_STATUS" != "202" ]]; then
  echo "Model load request failed with HTTP $LOAD_STATUS" >&2
  cat /tmp/talktomepy-load-response.json >&2 || true
  exit 1
fi

wait_for_model_ready

JSON_PAYLOAD="$(python3 - "$TEXT" "$INSTRUCT" "$LANGUAGE" <<'PY'
import json
import sys
text, instruct, language = sys.argv[1], sys.argv[2], sys.argv[3]
print(json.dumps({
    "text": text,
    "instruct": instruct,
    "language": language,
    "format": "wav",
}))
PY
)"

mkdir -p "$DEFAULT_OUTPUT_DIR"
TIMESTAMP="$(date +"%Y%m%d-%H%M%S")"
AUTO_SAVE_PATH="$DEFAULT_OUTPUT_DIR/tts-$TIMESTAMP.wav"
FINAL_PATH="$AUTO_SAVE_PATH"
if [[ -n "$SAVE_PATH" ]]; then
  mkdir -p "$(dirname "$SAVE_PATH")"
  FINAL_PATH="$SAVE_PATH"
fi

SYNTH_HEADERS="$(mktemp /tmp/talktomepy-tts-headers-XXXXXX.txt)"
attempt=1
while (( attempt <= MAX_SYNTH_RETRIES )); do
  HTTP_STATUS="$(curl -sS -D "$SYNTH_HEADERS" -o "$FINAL_PATH" -w "%{http_code}" -X POST "$BASE_URL/synthesize/voice-design" \
    -H "Content-Type: application/json" \
    -d "$JSON_PAYLOAD")"

  if [[ "$HTTP_STATUS" == "200" ]]; then
    break
  fi

  if [[ "$HTTP_STATUS" == "503" ]]; then
    RETRY_AFTER="$(awk 'tolower($1)=="retry-after:" {print $2}' "$SYNTH_HEADERS" | tr -d '\r' | tail -n 1)"
    if [[ -z "$RETRY_AFTER" ]]; then
      RETRY_AFTER="$DEFAULT_RETRY_AFTER_SECONDS"
    fi
    echo "Model still loading (HTTP 503). Retry $attempt/$MAX_SYNTH_RETRIES in ${RETRY_AFTER}s..." >&2
    sleep "$RETRY_AFTER"
    attempt=$((attempt + 1))
    continue
  fi

  echo "Synthesize failed with HTTP $HTTP_STATUS" >&2
  rm -f "$FINAL_PATH" "$SYNTH_HEADERS"
  exit 1
done

if [[ "$HTTP_STATUS" != "200" ]]; then
  echo "Synthesize failed after $MAX_SYNTH_RETRIES retries (last HTTP $HTTP_STATUS)" >&2
  rm -f "$FINAL_PATH" "$SYNTH_HEADERS"
  exit 1
fi

rm -f "$SYNTH_HEADERS"

echo "Generated WAV: $FINAL_PATH"
echo "Style: $STYLE"

if [[ "$PLAY_AUDIO" == "true" ]]; then
  afplay "$FINAL_PATH"
fi
