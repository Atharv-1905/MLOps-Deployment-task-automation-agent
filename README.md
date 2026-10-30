# AI Research Brief Generator

A lightweight Streamlit app that searches the web and generates a concise three-point research brief using a Groq-hosted OpenAI-compatible model.

## Features

- Web search with DuckDuckGo (`ddgs`)
- Two-stage workflow: search then summarize
- Streamlit UI for quick topic input and brief generation
- Docker support for containerized runs

## Project Structure

```text
.
├── app.py            # Streamlit application
├── requirements.txt  # Python dependencies
└── Dockerfile        # Container build and runtime setup
```

## Prerequisites

- Python 3.11+ (for local run)
- A Groq API key

## Environment Variables

Set the following variable before running:

- `GROQ_API_KEY` (required): API key used to call the Groq OpenAI-compatible endpoint
- `GROQ_MODEL` (optional): model name (default: `openai/gpt-oss-20b`)

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Export your API key:
   ```bash
   export GROQ_API_KEY="your_api_key_here"
   ```
4. Start the app:
   ```bash
   streamlit run app.py
   ```

## Docker Setup

Build the image:

```bash
docker build -t ai-research-brief .
```

Run the container:

```bash
docker run --rm -p 7860:7860 -e GROQ_API_KEY="your_api_key_here" ai-research-brief
```

## Usage

1. Open the app in your browser (typically `http://localhost:7860` locally or via mapped Docker port).
2. Enter a research topic.
3. Click **Generate Brief** to get exactly three summary bullet points.

## Notes

- If no search results are found, try a more specific query.
- If API credentials are missing, the app will return a configuration error.
