# app/pipeline_components.py
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

# List of features EXACTLY as the XGBoost model expects them
EXPECTED_FEATURES = [
    'open', 'high', 'low', 'close', 'volume', 'marketcap',
    'sma_7', 'sma_30', 'volatility_7', 'rsi_14',
    'high_lag_1', 'vol_lag_1', 'high_lag_2', 'vol_lag_2',
    'high_lag_3', 'vol_lag_3', 'high_lag_7', 'vol_lag_7'
]

def calculate_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    """Calculate RSI matching the notebook implementation."""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

class SolanaFeatureEngineer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        df = X.copy()
        
        # Standardize columns
        df.columns = df.columns.str.lower()
        
        # 1. Technical Indicators
        # Min_periods=1 ensures we get values even if window isn't full yet
        df["sma_7"] = df["close"].rolling(window=7, min_periods=1).mean()
        df["sma_30"] = df["close"].rolling(window=30, min_periods=1).mean()
        df["volatility_7"] = df["close"].rolling(window=7, min_periods=1).std()
        df["rsi_14"] = calculate_rsi(df["close"], window=14)
        
        # 2. Lag Features
        for lag in [1, 2, 3, 7]:
            df[f"high_lag_{lag}"] = df["high"].shift(lag)
            df[f"vol_lag_{lag}"] = df["volume"].shift(lag)
            
        # 3. Handling NaNs
        # Instead of dropping, we fill. 
        # For the very first rows, backfill is acceptable for inference to prevent crashes.
        df = df.ffill().bfill()
        
        # 4. Fill Marketcap if missing
        if 'marketcap' not in df.columns:
            df['marketcap'] = 0.0

        # Safety Check
        if df.empty:
            # If everything failed, return a DataFrame with 1 row of zeros 
            # (Emergency Fallback to prevent API 500 Error)
            return pd.DataFrame(0.0, index=[0], columns=EXPECTED_FEATURES)

        return df[EXPECTED_FEATURES]