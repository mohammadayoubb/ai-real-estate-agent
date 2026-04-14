import joblib
import pandas as pd
from pathlib import Path
import sys

import numpy.core.numeric as np_numeric
import numpy.random._pickle as np_pickle

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "best_house_price_model.pkl"


    
def _patch_numpy_bit_generator_loader():
    original_ctor = np_pickle.__bit_generator_ctor

    def compatible_ctor(bit_generator_name="MT19937"):
        if not isinstance(bit_generator_name, str) and hasattr(bit_generator_name, "__name__"):
            bit_generator_name = bit_generator_name.__name__
        return original_ctor(bit_generator_name)

    np_pickle.__bit_generator_ctor = compatible_ctor


_patch_numpy_bit_generator_loader()
sys.modules.setdefault("numpy._core.numeric", np_numeric)

model = None
model_load_error = None

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
    "totrms_abvgrd"
]

MODEL_COLUMN_MAPPING = {
    "gr_liv_area": "Gr Liv Area",
    "bedroom_abvgr": "Bedroom AbvGr",
    "full_bath": "Full Bath",
    "neighborhood": "Neighborhood",
    "overall_qual": "Overall Qual",
    "garage_cars": "Garage Cars",
    "year_built": "Year Built",
    "lot_area": "Lot Area",
    "house_style": "House Style",
    "totrms_abvgrd": "TotRms AbvGrd"
}

def can_predict(extracted_data: dict):
    missing_fields = [field for field in REQUIRED_FIELDS if extracted_data.get(field) is None]
    return len(missing_fields) == 0, missing_fields

def prepare_model_input(extracted_data: dict):
    model_ready_data = {}

    for schema_field, model_column in MODEL_COLUMN_MAPPING.items():
        model_ready_data[model_column] = extracted_data[schema_field]

    input_df = pd.DataFrame([model_ready_data])
    return input_df


def _get_model():
    global model
    global model_load_error

    if model is not None:
        return model

    if model_load_error is not None:
        raise RuntimeError(model_load_error)

    try:
        model = joblib.load(MODEL_PATH)
        return model
    except Exception as e:
        model_load_error = (
            f"Failed to load model from '{MODEL_PATH}': {e}. "
            "The model file exists, but it appears to be incompatible with the current NumPy/scikit-learn environment."
        )
        raise RuntimeError(model_load_error) from e

def predict_price(extracted_data: dict):
    is_ready, missing_fields = can_predict(extracted_data)

    if not is_ready:
        return {
            "prediction_ready": False,
            "missing_fields": missing_fields,
            "message": "Cannot run prediction because some required fields are missing."
        }

    try:
        input_df = prepare_model_input(extracted_data)
        prediction = _get_model().predict(input_df)[0]

        return {
            "prediction_ready": True,
            "predicted_price": round(float(prediction), 2),
            "missing_fields": []
        }

    except Exception as e:
        return {
            "prediction_ready": False,
            "error": str(e),
            "missing_fields": []
        }
