#!/bin/bash

# Check if two arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <originals_dir> <processed_dir>"
    exit 1
fi

ORIGINALS_DIR="$1"
PROCESSED_DIR="$2"

# Verify that the directories exist
if [ ! -d "$ORIGINALS_DIR" ]; then
    echo "Error: Originals directory does not exist: $ORIGINALS_DIR"
    exit 1
fi

if [ ! -d "$PROCESSED_DIR" ]; then
    echo "Error: Processed directory does not exist: $PROCESSED_DIR"
    exit 1
fi

# Initialize arrays
orig_files_array=()
proc_files_array=()

# Collect original files
for file in "$ORIGINALS_DIR"/*.wav; do
    if [ -f "$file" ]; then
        filename=$(basename "$file" .wav)
        orig_files_array+=("$filename")
    fi
done

# Collect processed files
for file in "$PROCESSED_DIR"/*.wav; do
    if [ -f "$file" ]; then
        filename=$(basename "$file" .wav)
        # Remove the '-enhanced-90p' suffix
        filename=${filename%-enhanced-90p}
        proc_files_array+=("$filename")
    fi
done

# Sort the arrays and write them to temporary files
orig_temp=$(mktemp)
proc_temp=$(mktemp)

printf "%s\n" "${orig_files_array[@]}" | sort > "$orig_temp"
printf "%s\n" "${proc_files_array[@]}" | sort > "$proc_temp"

# Find originals that are not in processed
missing_files=$(comm -23 "$orig_temp" "$proc_temp")

# Clean up temporary files
rm "$orig_temp" "$proc_temp"

# Output the missing original files
if [ -z "$missing_files" ]; then
    echo "All files have been processed."
else
    echo "Files not yet processed:"
    while IFS= read -r base; do
        echo "$ORIGINALS_DIR/$base.wav"
    done <<< "$missing_files"
fi
