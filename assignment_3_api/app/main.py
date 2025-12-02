# app/main.py
import joblib
import pandas as pd
import requests
from fastapi import FastAPI, HTTPException
from pathlib import Path
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Import the NEW pipeline
from app.pipeline_components import SolanaFeatureEngineer

# --- Config ---
MODEL_PATH = Path("models/xgboost_solana_v1.joblib")
COINGECKO_API = "https://api.coingecko.com/api/v3/coins/solana/ohlc"

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    if MODEL_PATH.exists():
        ml_models["model"] = joblib.load(MODEL_PATH)
        print(f"✅ Loaded model: {MODEL_PATH}")
    else:
        print(f"❌ Error: Model not found at {MODEL_PATH}")
    yield
    ml_models.clear()

app = FastAPI(title="Solana High Price Predictor", lifespan=lifespan)

class PredictionOut(BaseModel):
    token: str
    prediction_date: str
    predicted_high: float

def fetch_history():
    """Get 90 days of OHLC data from CoinGecko."""
    try:
        # Request 90 days to ensure enough data for 30-day SMA + Lags
        params = {"vs_currency": "usd", "days": "90"}
        resp = requests.get(COINGECKO_API, params=params)
        data = resp.json()
        
        # Convert to DataFrame (Timestamp, Open, High, Low, Close)
        df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close"])
        df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
        
        # Get Volume (Separate Call needed or approximate)
        # For simplicity/reliability in assignment, we can approximate or use a secondary call
        # Here we mock volume with a secondary call for full 'market_chart'
        chart_url = "https://api.coingecko.com/api/v3/coins/solana/market_chart"
        chart_data = requests.get(chart_url, params=params).json()
        
        vols = pd.DataFrame(chart_data['total_volumes'], columns=['timestamp', 'volume'])
        df = df.merge(vols, on='timestamp', how='left')
        
        return df
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Data provider error: {e}")

@app.get("/predict/solana", response_model=PredictionOut)
def predict():
    if "model" not in ml_models:
        raise HTTPException(500, "Model not active")
        
    # 1. Fetch
    raw_df = fetch_history()
    
    # 2. Process
    pipeline = SolanaFeatureEngineer()
    try:
        features_df = pipeline.transform(raw_df)
    except Exception as e:
        raise HTTPException(500, f"Pipeline Error: {e}")
        
    # 3. Predict (Use the LAST row = Today's data to predict Tomorrow)
    last_row = features_df.iloc[[-1]]
    prediction = ml_models["model"].predict(last_row)[0]
    
    # 4. Return
    tomorrow = raw_df.iloc[-1]["date"] + pd.Timedelta(days=1)
    
    return {
        "token": "SOL",
        "prediction_date": tomorrow.strftime("%Y-%m-%d"),
        "predicted_high": float(prediction)
    }