import json

from llm_chain import extract_features_stage1  
from predictor import predict_price
from interpreter import interpret_prediction


def run_full_pipeline(user_query: str):
    # Step 1: Extract features using LLM
    features = extract_features_stage1(user_query)

    # Handle extraction failure
    if isinstance(features, dict) and features.get("fallback"):
        return {
            "status": "error",
            "stage": "extraction",
            "details": features
        }

    # Step 2: Check completeness
    if not features.is_complete:
        return {
            "status": "incomplete",
            "missing_fields": features.missing_fields,
            "extracted_features": features.model_dump()
        }

    # Step 3: Run prediction
    prediction = predict_price(features.model_dump())

    if not prediction.get("prediction_ready"):
        return {
            "status": "error",
            "stage": "prediction",
            "details": prediction
        }

    # Step 4: Interpret result
    interpretation = interpret_prediction(prediction, features.model_dump())

    return {
        "status": "success",
        "features": features.model_dump(),
        "prediction": prediction,
        "interpretation": interpretation
    }


# ✅ ENTRY POINT (this is what was missing before)
if __name__ == "__main__":
    print("=== AI Real Estate Price Predictor ===\n")

    user_query = input("Enter house description:\n> ")

    result = run_full_pipeline(user_query)

    print("\n=== FINAL RESULT ===")
    print(json.dumps(result, indent=2))

    #input examples

    #A well-maintained 2-story family home with 2800 square feet of living space, 4 bedrooms, 3 full bathrooms, and a total of 9 rooms. The house has an overall quality rating of 8, includes a 2-car garage, and sits on a 9500 square foot lot. It was built in 2015 and is located in the desirable NridgHt neighborhood.

    #A large 2-story home with 3000 sqft, 5 bedrooms, 4 bathrooms, quality 8, 3-car garage, built in 2018, located in NridgHt, with 10 rooms and 12000 sqft lot.

    