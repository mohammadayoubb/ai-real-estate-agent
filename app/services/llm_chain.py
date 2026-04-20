import json
import os
import re

from pydantic import ValidationError

from app.core.prompts import stage1_prompt
from app.core.schemas import ExtractedFeatures
from app.paths import ENV_EXAMPLE_FILE, ENV_FILE

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


client = None

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
        load_dotenv(ENV_FILE)
        load_dotenv(ENV_EXAMPLE_FILE)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in environment or .env file.")

    if client is None:
        client = OpenAI(api_key=api_key)

    return client


def compute_completeness(data: dict):
    extracted_fields = [field for field in REQUIRED_FIELDS if data.get(field) is not None]
    missing_fields = [field for field in REQUIRED_FIELDS if data.get(field) is None]

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
                    "content": "You extract real estate features into strict JSON only. Return ONLY one JSON object. No markdown, no text.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        raw_output = response.choices[0].message.content.strip()

        print("\n=== RAW LLM OUTPUT ===")
        print(raw_output)
        print("======================\n")

        cleaned_output = re.sub(r"```json|```", "", raw_output).strip()
        match = re.search(r"\{.*\}", cleaned_output, re.DOTALL)

        if not match:
            return {
                "error": "No valid JSON object found in LLM output",
                "raw_output": raw_output,
                "fallback": True,
            }

        json_str = match.group(0)
        parsed_output = json.loads(json_str)

        if isinstance(parsed_output, list):
            if len(parsed_output) == 0:
                return {"error": "LLM returned empty list", "fallback": True}
            parsed_output = parsed_output[0]

        validated = ExtractedFeatures(**parsed_output)
        final_data = compute_completeness(validated.model_dump())

        return ExtractedFeatures(**final_data)

    except json.JSONDecodeError:
        return {"error": "Malformed JSON returned by LLM", "fallback": True}

    except ValidationError as e:
        return {
            "error": "Schema validation failed",
            "details": e.errors(),
            "fallback": True,
        }

    except Exception as e:
        return {"error": str(e), "fallback": True}
