import os
import docx2txt
import markdown
from pathlib import Path

def convert_word_to_markdown():
    # Define input and output paths
    input_file = "input/财富管理系列课程  v5.0(1).docx"
    output_dir = "data"
    output_file = "book_outline.md"  # Changed from .xlsx to .md
    
    # Create the output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)
    
    # Output file path
    output_path = os.path.join(output_dir, output_file)
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return
    
    print(f"Converting '{input_file}' to Markdown...")
    
    try:
        # Extract text from Word document
        text = docx2txt.process(input_file)
        
        # Save as Markdown
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"Conversion complete. Markdown saved to: {output_path}")
    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    convert_word_to_markdown() 