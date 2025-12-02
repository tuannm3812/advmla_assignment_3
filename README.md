# Advanced Data Product: Cryptocurrency Prediction

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36+-FF4B4B?logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-success)

![Hero Image](https://www.bankrate.com/2022/07/07151503/Cryptocurrency-statistics.jpeg?auto=webp&optimize=high&crop=16:9&width=912)

## 📖 Project Overview

This project is a comprehensive Data Product designed to assist cryptocurrency investors. It combines historical market data with machine learning predictions to forecast the **Next-Day High Price** of major tokens.

The architecture is split into three core components:
1.  **Experimentation:** Jupyter notebooks for EDA, Feature Engineering, and Model Training (XGBoost/LightGBM).
2.  **API Backend:** A FastAPI service deployed on Render to serve ML predictions.
3.  **Dashboard UI:** A Streamlit application visualizing real-time Kraken data and AI forecasts.

---

## 🏗️ Repository Structure

This repository is organized as a monorepo containing both the backend and frontend services.

```text
advmla_assignment_3/
├── assignment_3_api/       # 🧠 Backend: FastAPI Service
│   ├── app/                # Application Logic & Pipelines
│   ├── models/             # Trained Model Artifacts (.joblib)
│   └── Dockerfile          # Container config for Render
│
├── assignment_3_streamlit/ # 💻 Frontend: User Interface
│   ├── app/
│   │   ├── students/       # Individual Student Components
│   │   └── main.py         # App Entry Point
│   └── Dockerfile
│
├── notebooks/              # 🔬 Experimentation & Training
│   └── Solana_XGBoost.ipynb
│
└── models/                 # Shared Model Storage
```

🪙 Supported Assets & Status

This project is a group effort. Below is the status of each cryptocurrency module.

| Asset    | Symbol | Status        | Assignee         | Model               |
|---------:|:------:|:-------------:|:----------------:|:-------------------:|
| Solana   | SOL    | ✅ Live        | Student 25739083 | XGBoost Regressor   |
| Bitcoin  | BTC    | 🚧 In Progress | Group Member     | Pending             |
| Ethereum | ETH    | 🚧 In Progress | Group Member     | Pending             |
| Ripple   | XRP    | 🚧 In Progress | Group Member     | Pending             |

## 🚀 Quick Start Guide
1. Clone the Repository

```bash
git clone https://github.com/YourUsername/advmla_assignment_3.git
cd advmla_assignment_3
```

2. Running the API (Backend)

The UI relies on the API for predictions. Run this first.

```bash
cd assignment_3_api
# Install Dependencies
pip install -r requirements.txt
# Run Server
uvicorn app.main:app --reload --port 8000
```

API will be available at: http://localhost:8000

3. Running the Dashboard (Frontend)

Open a new terminal window for the UI.

```bash
cd assignment_3_streamlit
# Install Dependencies
pip install -r requirements.txt
# Run Streamlit
streamlit run app/main.py
```

Dashboard will open at: http://localhost:8501

## 🛠️ Tech Stack
Language: Python 3.11

Machine Learning: XGBoost, Hyperopt, Scikit-Learn

Web Frameworks: FastAPI, Streamlit

Data Sources: CoinGecko API (History), Kraken API (Real-time)

DevOps: Docker, Render
