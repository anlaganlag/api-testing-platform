# Book Generator

This project helps you generate a book by using an LLM (Large Language Model) to expand on chapter outlines specified in an Excel file.

## Setup

1. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

2. Set up your API keys:
Create a `.env` file in the project root based on the `.env.example` template.

## Preparing Your Book Outline

1. Create an Excel file with the following columns:
   - `课程模块`: Module name
   - `课程主题`: Topic title 
   - `课程大纲`: Content outline
   - `内容说明`: Content description

Place this file in the `data` directory as `book_outline.xlsx`.

## Generating the Book

### Local Generation

Run the book generator:
```bash
python src/enhanced_book_generator_fixed.py --excel data/book_outline.xlsx --provider all
```

To generate a sample chapter:
```bash
python src/enhanced_book_generator_fixed.py --excel data/book_outline.xlsx --provider all --sample 0
```

### Web Interface via Vercel

This project can be deployed to Vercel as a serverless application.

## Deploying to Vercel

### Prerequisites

1. A [Vercel](https://vercel.com) account
2. The [Vercel CLI](https://vercel.com/docs/cli) installed (optional for deployments via GitHub)

### Deployment Steps

#### Option 1: Deploy via GitHub

1. Push your project to GitHub
2. Connect Vercel to your GitHub repository
3. Configure environment variables in the Vercel dashboard:
   - Add all API keys and URLs from your `.env` file
4. Deploy the project

#### Option 2: Deploy via Vercel CLI

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy the project:
```bash
vercel
```

4. Follow the prompts to set up your project
5. Configure environment variables when prompted or in the Vercel dashboard

### Environment Variables

You'll need to set the following environment variables in Vercel:

- `DEEPSEEK_API_KEY`, `DEEPSEEK_API_URL`, `DEEPSEEK_API_MODEL`
- `GEMINI_API_KEY`, `GEMINI_API_URL`, `GEMINI_API_MODEL`
- `OPENROUTER_API_KEY`, `OPENROUTER_API_URL`, `OPENROUTER_MODEL`
- `SILICONFLOW_API_KEY`, `SILICONFLOW_API_URL`, `SILICONFLOW_MODEL`
- `ARK_API_KEY`, `ARK_API_URL`, `ARK_MODEL`
- `DASHSCOPE_API_KEY`, `DASHSCOP_API_URL`, `DASHSCOP_MODEL`

You can use Vercel's UI to add these environment variables or use the following CLI command:

```bash
vercel env add DEEPSEEK_API_KEY
```

### Usage After Deployment

After deployment, you'll have:
- A web interface at `https://your-vercel-url.vercel.app/`
- A REST API endpoint at `https://your-vercel-url.vercel.app/api/generate`

## Output

Generated content will be saved in the `output` directory:
- Individual chapter files in Markdown format
- Complete book in Word format (for local generation)

## Notes

- The generator supports multiple API providers with fallback
- Each section aims for approximately 800-1000 words
- The system maintains cache to avoid repeated API calls
- Make sure your API keys have sufficient credits 