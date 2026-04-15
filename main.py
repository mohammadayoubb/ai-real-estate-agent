from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict

from llm_chain import extract_features_stage1
from predictor import predict_price
from interpreter import interpret_prediction  # change to interpreter if you renamed the file

app = FastAPI(
    title="AI Real Estate Agent API",
    description="Natural language property input -> feature extraction -> price prediction -> interpretation",
    version="1.0.0"
)


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {
        "message": "AI Real Estate Agent API is running"
    }


@app.post("/predict")
def predict(request: QueryRequest):
    user_query = request.query.strip()

    if not user_query:
        return {
            "status": "error",
            "stage": "input",
            "details": {
                "message": "Query cannot be empty."
            }
        }

    # Stage 1: LLM extraction
    features = extract_features_stage1(user_query)

    if isinstance(features, dict) and features.get("fallback"):
        return {
            "status": "error",
            "stage": "extraction",
            "details": features
        }

    features_data = features.model_dump()

    # Check completeness before prediction
    if not features.is_complete:
        return {
            "status": "incomplete",
            "message": "Some required features are missing. Please provide or fill them before prediction.",
            "features": features_data,
            "missing_fields": features.missing_fields
        }

    # Stage 2: ML prediction
    prediction = predict_price(features_data)

    if not prediction.get("prediction_ready"):
        return {
            "status": "error",
            "stage": "prediction",
            "features": features_data,
            "details": prediction
        }

    predicted_price = prediction["predicted_price"]

    # Stage 3: LLM interpretation
    interpretation = interpret_prediction(features_data, predicted_price)

    if not interpretation.get("interpretation_ready"):
        return {
            "status": "error",
            "stage": "interpretation",  
            "features": features_data,
            "prediction": prediction,
            "details": interpretation
        }

    return {
        "status": "success",
        "features": features_data,
        "prediction": prediction,
        "interpretation": interpretation
    }

    #input examples

    #A well-maintained 2-story family home with 2800 square feet of living space, 4 bedrooms, 3 full bathrooms, and a total of 9 rooms. The house has an overall quality rating of 8, includes a 2-car garage, and sits on a 9500 square foot lot. It was built in 2015 and is located in the desirable NridgHt neighborhood.

    #A large 2-story home with 3000 sqft, 5 bedrooms, 4 bathrooms, quality 8, 3-car garage, built in 2018, located in NridgHt, with 10 rooms and 12000 sqft lot.

