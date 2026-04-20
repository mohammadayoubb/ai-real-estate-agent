import json

from app.services.llm_chain import extract_features_stage1
from app.services.predictor import predict_price


query = "A 2Story 4-bedroom home with 2500 square feet, 3 bathrooms, in NAmes, with a 2-car garage, built in 2012, 8 total rooms, lot area 9000 square feet, and overall quality 7."

extracted = extract_features_stage1(query)

if isinstance(extracted, dict):
    print("Extraction failed:")
    print(json.dumps(extracted, indent=2))
else:
    extracted_data = extracted.model_dump()

    print("\nExtracted Features:")
    print(json.dumps(extracted_data, indent=2))

    prediction_result = predict_price(extracted_data)

    print("\nPrediction Result:")
    print(json.dumps(prediction_result, indent=2))
