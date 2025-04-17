# Book Generator

This project helps you generate a book by using an LLM (Large Language Model) to expand on chapter outlines specified in an Excel file.

## Setup

1. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

2. Set up your OpenAI API key:
Create a `.env` file in the project root with:
```
OPENAI_API_KEY=your_api_key_here
```

## Preparing Your Book Outline

1. Create an Excel file with the following columns:
   - `chapter_number`: The sequential number of the chapter
   - `chapter_title`: The title of the chapter
   - `chapter_outline`: A detailed outline of what the chapter should cover

You can generate a sample template by running:
```bash
python src/create_template.py
```

## Generating the Book

1. Place your Excel file in the `data` directory
2. Run the book generator:
```bash
python src/book_generator.py
```

The generator will:
- Read your chapter outlines
- Generate approximately 3500 words per chapter using GPT-4
- Maintain consistency between chapters
- Save each chapter as a separate text file in the `output` directory
- Create a metadata file with information about all generated chapters

## Output

Generated content will be saved in the `output` directory:
- Individual chapter files: `chapter_XX.txt`
- Book metadata: `book_metadata.json`

## Notes

- The generator uses GPT-4 to ensure high-quality content
- Each chapter aims for 3000-4000 words
- The system maintains context between chapters for consistency
- Make sure your OpenAI API key has sufficient credits 