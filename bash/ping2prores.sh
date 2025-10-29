#!/usr/bin/env bash
#
# Converts a sequence of PNG images into a ProRes 422 video.
# Usage:
#   ./png2prores.sh <FRAMERATE> <INPUT_PATTERN> <OUTPUT_FILE>
#
# Example:
#   ./png2prores.sh 24 img%04d.png output.mov

# Exit on error
set -e

if [ $# -lt 3 ]; then
  echo "Usage: $0 <FRAMERATE> <INPUT_PATTERN> <OUTPUT_FILE>"
  echo "Example: $0 24 image%04d.png output.mov"
  exit 1
fi

FRAMERATE="$1"
INPUT_PATTERN="$2"
OUTPUT_FILE="$3"

# The -profile:v 3 corresponds to ProRes 422 standard quality
# Adjust -profile:v as needed:
#   0: proxy
#   1: LT
#   2: 422
#   3: HQ
#   4: 4444
#   5: 4444 alpha
#
# -pix_fmt yuv422p10le is the standard pixel format for ProRes 422.

ffmpeg -y \
  -framerate "$FRAMERATE" \
  -i "$INPUT_PATTERN" \
  -c:v prores_ks \
  -profile:v 2 \
  -pix_fmt yuv422p10le \
  "$OUTPUT_FILE"
