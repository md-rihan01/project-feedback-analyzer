# Project Feedback Analyzer

A small customer feedback analyzer with a Streamlit dashboard and a FastAPI backend. Enter reviews in the dashboard (one per line) to get a sentiment label, a 1–5 score, and a one-word topic for each review. The dashboard also shows an overall score and positive-review percentage.

## Run after cloning

Clone the GitHub repository, then change into its `code` directory. Replace `<repository-url>` with the URL shown on the repository's GitHub page:

```bash
git clone <repository-url>
cd project-feedback-analyzer/code
```

Install dependencies and configure the Gemini API key as described below. Start the API and dashboard in separate terminals using the commands in [Run the application](#run-the-application).

## Requirements

- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/)
- A Google Gemini API key

## Setup

From the `code` directory, install the project dependencies:

```bash
uv sync
```

Set your Gemini key in a `.env` file in the project root or in the `code` directory:

```dotenv
GOOGLE_API_KEY=your_gemini_api_key
```

The Google Gen AI client reads `GOOGLE_API_KEY` when it creates the client. Keep the key private and do not commit it.

## Run the application

Start the API from the `code` directory:

```bash
uv run uvicorn api:app --reload
```

In a second terminal, also from the `code` directory, start the dashboard:

```bash
uv run streamlit run app.py
```

Open the local URL printed by Streamlit. The dashboard sends each non-empty review to `http://127.0.0.1:8000/analyze`, so keep the API running while using it.

## API

`POST /analyze` accepts a JSON object containing the review text:

```json
{
  "text": "The food was delicious, but delivery was late."
}
```

It returns JSON with these fields:

```json
{
  "label": "neutral",
  "score": 3,
  "theme": "delivery"
}
```

The label is `positive`, `negative`, or `neutral`; the score ranges from 1 to 5; and the theme is one lowercase word.

## Sample reviews

`sample_reviews.txt` contains example customer reviews you can paste into the dashboard. Enter one review per line.
