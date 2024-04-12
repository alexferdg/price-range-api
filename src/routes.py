# Endpoints implementation
from fastapi import APIRouter, Depends, HTTPException, status
from models import MobileCharacteristics, PricePredictionResponse
from dependencies import load_model
import numpy as np

router = APIRouter()

# GET /v1/price_range
@router.get("/v1/price_range", response_description="Price range prediction", status_code=status.HTTP_200_OK, response_model = PricePredictionResponse)
def mobile_price_range(
    characteristics: MobileCharacteristics = Depends(),
    model_id: str = "default_model_id",
    model: callable = Depends(load_model)
    ):

    # Features for model prediction
    features = np.array([value for value in characteristics.model_dump().values()])
    result = model.predict(features.reshape(1, -1))
    try:
        result = model.predict(features.reshape(1, -1))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # Decode results
    price_ranges = ["Low cost", "Medium cost", "High cost", "Very high cost"]
    pretty_result = price_ranges[int(result[0])] if int(result[0]) in range(4) else "Unknown"

    return {"price_range": pretty_result, "model_used": model_id}
