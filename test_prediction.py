import json
from llm_chain import extract_features_stage1
from predictor import predict_price

query = "A 2Story 4-bedroom home with 2500 square feet, 3 bathrooms, in NAmes, with a 2-car garage, built in 2012, 8 total rooms, lot area 9000 square feet, and overall quality 7."

#query='A modern 4-bedroom home with a big garage in a nice neighborhood.'

#query='A 2Story home in Gilbert with 3200 square feet, 5 bedrooms, 4 full bathrooms, overall quality 9, 3 garage spaces, built in 2018, lot area 12000 square feet, and 10 total rooms above ground.'

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