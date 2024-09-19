#!/bin/bash

# Function to display usage instructions
usage() {
    echo "Usage: $0 -i input_file -o output_mask -d destination_path -s start_frame -e end_frame"
    echo "Example: $0 -i blank.png -o frame_%04d.png -d /path/to/destination -s 1 -e 464"
    exit 1
}

# Parse command-line arguments
while getopts ":i:o:d:s:e:" opt; do
    case "${opt}" in
        i)
            input_file=${OPTARG}
            ;;
        o)
            output_mask=${OPTARG}
            ;;
        d)
            destination_path=${OPTARG}
            ;;
        s)
            start_frame=${OPTARG}
            ;;
        e)
            end_frame=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done

# Check for mandatory arguments
if [[ -z "${input_file}" || -z "${output_mask}" || -z "${destination_path}" || -z "${start_frame}" || -z "${end_frame}" ]]; then
    usage
fi

# Create the destination directory if it doesn't exist
mkdir -p "${destination_path}"

# Loop to copy the input file to the destination path with the sequential naming
for ((i = start_frame; i <= end_frame; i++)); do
    output_file=$(printf "${output_mask}" "${i}")
    cp "${input_file}" "${destination_path}/${output_file}"
done

echo "Files created successfully."