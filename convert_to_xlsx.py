import os
import shutil
from pathlib import Path

def copy_markdown_to_xlsx():
    # Define file paths
    source_file = "data/book_outline.md"
    target_file = "data/book_outline.xlsx"
    
    # Check if source file exists
    if not os.path.exists(source_file):
        print(f"Error: Source file '{source_file}' not found.")
        return
    
    try:
        # Copy the file content
        shutil.copy2(source_file, target_file)
        
        print(f"File copied successfully: {target_file}")
    except Exception as e:
        print(f"Error during file copy: {e}")

if __name__ == "__main__":
    copy_markdown_to_xlsx() 