import re
import sys
import os

def clean_transcript(input_file, output_file):
    """
    Cleans up a transcript file by removing:
    - Empty lines
    - Line numbers
    - Timestamps
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        cleaned_lines = []
        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue
            
            # Skip lines that are just numbers (line numbers)
            if line.strip().isdigit():
                continue
            
            # Skip timestamp lines (format: 00:00:00,000 --> 00:00:00,000)
            if re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line.strip()):
                continue
            
            cleaned_lines.append(line)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_lines)
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clean_transcript.py <input_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    # Get the directory and filename from the input path
    input_dir = os.path.dirname(input_file)
    input_filename = os.path.basename(input_file)
    
    # Create output filename with 'cleaned_' prefix
    output_filename = f"cleaned_{input_filename}"
    output_file = os.path.join(input_dir, output_filename)
    
    clean_transcript(input_file, output_file)
    print(f"Transcript cleaned and saved to: {output_file}") 