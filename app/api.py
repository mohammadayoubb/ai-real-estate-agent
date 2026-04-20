from fastapi import FastAPI
from pydantic import BaseModel

from app.services.interpreter import interpret_prediction
from app.services.llm_chain import extract_features_stage1
from app.services.predictor import predict_price


app = FastAPI(
    title="AI Real Estate Agent API",
    description="Natural language property input -> feature extraction -> price prediction -> interpretation",
    version="1.0.0",
)


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {"message": "AI Real Estate Agent API is running"}


@app.post("/predict")
def predict(request: QueryRequest):
    user_query = request.query.strip()

    if not user_query:
        return {
            "status": "error",
            "stage": "input",
            "details": {"message": "Query cannot be empty."},
        }

    features = extract_features_stage1(user_query)

    if isinstance(features, dict) and features.get("fallback"):
        return {
            "status": "error",
            "stage": "extraction",
            "details": features,
        }

    features_data = features.model_dump()

    if not features.is_complete:
        return {
            "status": "incomplete",
            "message": "Some required features are missing. Please provide or fill them before prediction.",
            "features": features_data,
            "missing_fields": features.missing_fields,
        }

    prediction = predict_price(features_data)

    if not prediction.get("prediction_ready"):
        return {
            "status": "error",
            "stage": "prediction",
            "features": features_data,
            "details": prediction,
        }

    predicted_price = prediction["predicted_price"]
    interpretation = interpret_prediction(features_data, predicted_price)

    if not interpretation.get("interpretation_ready"):
        return {
            "status": "error",
            "stage": "interpretation",
            "features": features_data,
            "prediction": prediction,
            "details": interpretation,
        }

    return {
        "status": "success",
        "features": features_data,
        "prediction": prediction,
        "interpretation": interpretation,
    }
