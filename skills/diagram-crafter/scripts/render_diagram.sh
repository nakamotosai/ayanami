#!/usr/bin/env bash
set -euo pipefail

usage(){
  cat <<'EOF'
Usage: $0 -i <mermaid-file> [-o <output.png>] [-w width] [-h height]

Reads a Mermaid definition and renders it to PNG using mmdc.
EOF
  exit 1
}

INPUT=""
OUTPUT="diagram.png"
WIDTH=1024
HEIGHT=768

while [[ $# -gt 0 ]]; do
  case "$1" in
    -i|--input)
      INPUT="$2"
      shift 2
      ;;
    -o|--output)
      OUTPUT="$2"
      shift 2
      ;;
    -w|--width)
      WIDTH="$2"
      shift 2
      ;;
    -h|--height)
      HEIGHT="$2"
      shift 2
      ;;
    -h|--help)
      usage
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      ;;
  esac
done

if [[ -z "$INPUT" ]]; then
  echo "Input file is required." >&2
  usage
fi

if [[ ! -f "$INPUT" ]]; then
  echo "Input file does not exist: $INPUT" >&2
  exit 1
fi

PATH="$PATH:/home/ubuntu/.npm-global/bin"
mmdc -i "$INPUT" -o "$OUTPUT" -w "$WIDTH" -H "$HEIGHT" >/dev/null 2>&1

echo "Rendered diagram to $OUTPUT"
