#!/usr/bin/env bash
set -euo pipefail

# Usage: ./transcribe.sh [input_file]
# Define the input file variable (no spaces around =). Allow override via arg 1.
file="${1:?Error: Please provide an input file as the first argument}"

# Ensure the input exists
if [[ ! -f "$file" ]]; then
  echo "Input not found: $file" >&2
  exit 1
fi

# Ensure output directory exists
outdir="./transcribe"
mkdir -p "$outdir"

# Quiet via flag
whisper "$file" \
  --model large \
  --language en \
  --task transcribe \
  --output_dir "$outdir" \
  --output_format all \
  --verbose False