#!/bin/bash

set -e

INPUT_DIR="/film_projects/kanashimi/footage/FX-ELEMENTS/stills/dead-randy-reference/pano"
MERGED_DIR="/film_projects/kanashimi/footage/FX-ELEMENTS/stills/dead-randy-reference/pano/merged_hdrs"
COMPRESSED_DIR="/film_projects/kanashimi/footage/FX-ELEMENTS/stills/dead-randy-reference/pano/compressed_hdrs"
BACKUP_DIR="/film_projects/kanashimi/footage/FX-ELEMENTS/stills/dead-randy-reference/pano/dng_backup"

mkdir -p "$MERGED_DIR" "$COMPRESSED_DIR" "$BACKUP_DIR"

# Get unique prefix groups
prefixes=$(find "$INPUT_DIR" -type f -iname '*.dng' | \
  sed -E 's/(-[1-9])\.dng$//' | sort | uniq)

for prefix in $prefixes; do
    base=$(basename "$prefix")
    echo "👉 Processing bracket set: $base-[1-3].dng"

    files=("$prefix"-1.dng "$prefix"-2.dng "$prefix"-3.dng)

    for f in "${files[@]}"; do
        if [ ! -f "$f" ]; then
            echo "❌ Missing file: $f"
            continue 2
        fi
    done

    # Merge to full EXR
    MERGED_EXR="$MERGED_DIR/$base.exr"
    hdrmerge --align --output="$MERGED_EXR" "${files[@]}"
    echo "✅ Merged: $MERGED_EXR"

    # Compress with DWAB
    COMPRESSED_EXR="$COMPRESSED_DIR/$base.exr"
    oiiotool "$MERGED_EXR" --compression dwab -o "$COMPRESSED_EXR"
    echo "🎯 Compressed: $COMPRESSED_EXR"

    # Archive dngs
    for f in "${files[@]}"; do
        mv "$f" "$BACKUP_DIR/"
    done
    echo "📦 Moved original dngs to $BACKUP_DIR"
done

echo "🏁 All done! You’ll find your DWAB EXRs in $COMPRESSED_DIR"
