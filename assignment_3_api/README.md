# 🚀 Solana Price Prediction API (AT3)

This project contains a **FastAPI** application that serves a Machine Learning model (XGBoost) to predict the **High Price** of Solana (SOL) for the next day ($t+1$).

## 📋 Features
- **Model:** XGBoost Regressor (Optimized via Hyperopt).
- **Data Source:** Fetches live OHLCV data via CoinGecko API.
- **Preprocessing:** Custom Scikit-learn pipeline matching the experimentation phase.
- **Deployment:** Dockerized for deployment on Render.

## 🛠️ Project Structure
```text
assignment_3_api/
├── app/
│   ├── main.py                # API Endpoints & Logic
│   ├── pipeline_components.py # Feature Engineering (must match Notebook)
│   └── __init__.py
├── models/
│   └── xgboost_solana_v1.joblib  # Trained Model Artifact
├── Dockerfile                 # Docker configuration
├── requirements.txt           # Python dependencies
└── README.md                  # Documentation