#!/bin/bash

# Check if a file path was provided
if [ $# -eq 0 ]; then
    echo "Please provide the path to the JSON file"
    echo "Usage: ./json_to_txt.sh /path/to/your/file.json"
    exit 1
fi

# Get the input file path
input_file="$1"

# Check if the file exists
if [ ! -f "$input_file" ]; then
    echo "Error: File '$input_file' not found"
    exit 1
fi

# Get the directory and filename without extension
dir_path=$(dirname "$input_file")
filename=$(basename "$input_file" .json)

# Create the output file path
output_file="${dir_path}/${filename}.txt"

# Convert JSON to text
jq -r '.[].sentence' "$input_file" > "$output_file"

# Check if conversion was successful
if [ $? -eq 0 ]; then
    echo "Successfully converted $input_file to $output_file"
else
    echo "Error converting file"
    exit 1
fi 