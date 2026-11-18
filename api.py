
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types
import traceback

load_dotenv()

client = genai.Client()

app = FastAPI()


class Review(BaseModel):
    text: str


class Analysis(BaseModel):
    label: str
    score: int
    theme: str


@app.post("/analyze")
def analyze(review: Review):

    try:
        response = client.models.generate_content(
            model="gemini-4-hydrogen",
            contents=(
                "Analyze this customer review.\n"
                "label must be one of: positive, negative, neutral.\n"
                "score must be a number from 1 to 5.\n"
                "theme must be ONE lowercase word for the main topic.\n"
                f"Review: {review.text}"
            ),
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=Analysis,
            ),
        )

        if response.parsed is None:
            raise ValueError("Gemini returned an empty or unparsed response.")

        return response.parsed

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
