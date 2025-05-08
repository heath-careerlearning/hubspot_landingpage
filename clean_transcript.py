import re
import sys
import os
import shutil

def combine_transcripts(file1, file2, output_file):
    """
    Combines two SRT files into one text file.
    First copies file1 to output_file, then appends file2's content.
    """
    try:
        # Copy first file to output file
        shutil.copy2(file1, output_file)
        
        # Append second file's content
        with open(file2, 'r', encoding='utf-8') as f2:
            content2 = f2.read()
            
        with open(output_file, 'a', encoding='utf-8') as out:
            out.write('\n' + content2)
            
        return output_file
    except Exception as e:
        print(f"Error combining files: {str(e)}")
        sys.exit(1)

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
                
            # Skip simple timestamp lines (format: 00:00:00 or 00:00)
            if re.match(r'^(\d{2}:\d{2}:\d{2}|\d{2}:\d{2})$', line.strip()):
                continue
                
            # Skip speaker lines
            if re.match(r'^Speaker \d+$', line.strip()):
                continue
            
            cleaned_lines.append(line)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_lines)
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_transcript.py <input_file> [second_file]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    # Get the directory and filename from the input path
    input_dir = os.path.dirname(input_file)
    input_filename = os.path.basename(input_file)
    
    # If second file is provided, combine them first
    if len(sys.argv) == 3:
        second_file = sys.argv[2]
        # Create temporary combined file
        temp_combined = os.path.join(input_dir, f"temp_combined_{input_filename}")
        combined_file = combine_transcripts(input_file, second_file, temp_combined)
        input_file = combined_file
    
    # Create output filename with 'cleaned_' prefix and .txt extension
    base_name = os.path.splitext(input_filename)[0]  # Remove original extension
    output_filename = f"cleaned_{base_name}.txt"
    output_file = os.path.join(input_dir, output_filename)
    
    clean_transcript(input_file, output_file)
    
    # Clean up temporary combined file if it was created
    if len(sys.argv) == 3 and os.path.exists(temp_combined):
        os.remove(temp_combined)
        
    print(f"Transcript cleaned and saved to: {output_file}") 