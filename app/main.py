from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from typing import List

app = FastAPI()

#model = joblib.load("model.pkl")
model = joblib.load("model.pkl")

class PredictionRequest(BaseModel):
    data: List[float]

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    return {"status": "ready"}

@app.post("/predict")
def custom_predict(request: PredictionRequest):
    prediction = model.predict([request.data])
    return {"prediction": int(prediction[0])}

#Test Workflow
