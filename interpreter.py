import os
import joblib
from dotenv import load_dotenv
from openai import OpenAI
from prompts import stage2_prompt

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SUMMARY_STATS_PATH = "summary_stats.pkl"
summary_stats = joblib.load(SUMMARY_STATS_PATH)


def interpret_prediction(features: dict, predicted_price: float):
    prompt = stage2_prompt.format(
        features=features,
        predicted_price=predicted_price,
        summary_stats=summary_stats
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You explain real estate price predictions clearly and accurately."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        interpretation = response.choices[0].message.content.strip()

        return {
            "interpretation_ready": True,
            "interpretation": interpretation
        }

    except Exception as e:
        return {
            "interpretation_ready": False,
            "error": str(e)
        }