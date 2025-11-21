#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: $0 <input_file> <output_file>"
    exit 1
fi

INPUT="$1"
OUTPUT="$2"
TARGET_SIZE_MB=2

# Calculate duration
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$INPUT")

if [ -z "$DURATION" ]; then
    echo "Error: Could not determine video duration"
    exit 1
fi

# Calculate target bitrate (in kbps)
TARGET_SIZE_BITS=$((TARGET_SIZE_MB * 8192 * 1024))
VIDEO_BITRATE=$((TARGET_SIZE_BITS / ${DURATION%.*} / 1000))

echo "Duration: ${DURATION}s"
echo "Target bitrate: ${VIDEO_BITRATE}kbps"

# Two-pass encoding
echo "Pass 1/2..."
ffmpeg -y -i "$INPUT" -c:v libx264 -b:v ${VIDEO_BITRATE}k -pass 1 -an -f null /dev/null

echo "Pass 2/2..."
ffmpeg -y -i "$INPUT" -c:v libx264 -b:v ${VIDEO_BITRATE}k -pass 2 -an "$OUTPUT"

# Cleanup
rm -f ffmpeg2pass-0.log ffmpeg2pass-0.log.mbtree

echo "Done: $OUTPUT"
