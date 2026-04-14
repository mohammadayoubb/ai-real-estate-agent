import json
from interpreter import interpret_prediction

features = {
    "gr_liv_area": 2500.0,
    "bedroom_abvgr": 4,
    "full_bath": 3,
    "neighborhood": "NAmes",
    "overall_qual": 7,
    "garage_cars": 2,
    "year_built": 2012,
    "lot_area": 9000.0,
    "house_style": "2Story",
    "totrms_abvgrd": 8
}

predicted_price = 272757.14

result = interpret_prediction(features, predicted_price)
print(json.dumps(result, indent=2))