import json
import os
import re
from pathlib import Path
from pydantic import ValidationError

from prompts import stage1_prompt
from schemas import ExtractedFeatures

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


client = None
BASE_DIR = Path(__file__).resolve().parent

REQUIRED_FIELDS = [
    "gr_liv_area",
    "bedroom_abvgr",
    "full_bath",
    "neighborhood",
    "overall_qual",
    "garage_cars",
    "year_built",
    "lot_area",
    "house_style",
    "totrms_abvgrd",
]


def _get_client():
    global client

    if OpenAI is None:
        raise RuntimeError("Missing dependency: install the `openai` package.")

    if load_dotenv is not None:
        load_dotenv(BASE_DIR / ".env")
        load_dotenv(BASE_DIR / ".env.example")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in environment or .env file.")

    if client is None:
        client = OpenAI(api_key=api_key)

    return client


def compute_completeness(data: dict):
    extracted_fields = [f for f in REQUIRED_FIELDS if data.get(f) is not None]
    missing_fields = [f for f in REQUIRED_FIELDS if data.get(f) is None]

    data["extracted_fields"] = extracted_fields
    data["missing_fields"] = missing_fields
    data["is_complete"] = len(missing_fields) == 0

    return data


def extract_features_stage1(user_query: str):
    prompt = stage1_prompt.format(user_query=user_query)

    try:
        response = _get_client().chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You extract real estate features into strict JSON only. Return ONLY one JSON object. No markdown, no text."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        raw_output = response.choices[0].message.content.strip()

        # Debug (keep for now)
        print("\n=== RAW LLM OUTPUT ===")
        print(raw_output)
        print("======================\n")

        # Remove markdown (```json)
        cleaned_output = re.sub(r"```json|```", "", raw_output).strip()

        # Extract JSON object
        match = re.search(r"\{.*\}", cleaned_output, re.DOTALL)

        if not match:
            return {
                "error": "No valid JSON object found in LLM output",
                "raw_output": raw_output,
                "fallback": True
            }

        json_str = match.group(0)
        parsed_output = json.loads(json_str)

        # Handle list case
        if isinstance(parsed_output, list):
            if len(parsed_output) == 0:
                return {
                    "error": "LLM returned empty list",
                    "fallback": True
                }
            parsed_output = parsed_output[0]

        # Validate
        validated = ExtractedFeatures(**parsed_output)

        # Add completeness info
        final_data = compute_completeness(validated.model_dump())

        return ExtractedFeatures(**final_data)

    except json.JSONDecodeError:
        return {
            "error": "Malformed JSON returned by LLM",
            "fallback": True
        }

    except ValidationError as e:
        return {
            "error": "Schema validation failed",
            "details": e.errors(),
            "fallback": True
        }

    except Exception as e:
        return {
            "error": str(e),
            "fallback": True
        }