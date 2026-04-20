import os

import joblib
from openai import OpenAI

from app.core.prompts import stage2_prompt
from app.paths import DATA_DIR, ENV_EXAMPLE_FILE, ENV_FILE

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


SUMMARY_STATS_PATH = DATA_DIR / "summary_stats.pkl"
summary_stats = joblib.load(SUMMARY_STATS_PATH)
client = None


def _get_client():
    global client

    if load_dotenv is not None:
        load_dotenv(ENV_FILE)
        load_dotenv(ENV_EXAMPLE_FILE)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in environment or .env file.")

    if client is None:
        client = OpenAI(api_key=api_key)

    return client


def interpret_prediction(features: dict, predicted_price: float):
    prompt = stage2_prompt.format(
        features=features,
        predicted_price=predicted_price,
        summary_stats=summary_stats,
    )

    try:
        response = _get_client().chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You explain real estate price predictions clearly and accurately.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.3,
        )

        interpretation = response.choices[0].message.content.strip()

        return {
            "interpretation_ready": True,
            "interpretation": interpretation,
        }

    except Exception as e:
        return {
            "interpretation_ready": False,
            "error": str(e),
        }
