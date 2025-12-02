# app/students/sol_25739083.py
import sys
from pathlib import Path

# Fix import path for utils
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st
import plotly.graph_objects as go
import requests
import pandas as pd
from datetime import datetime
from utils import fetch_kraken_data

# API Config
API_URL = "http://127.0.0.1:8000"  # Change to your Render URL for production

def render_solana_tab():
    # --- Title Section ---
    st.markdown("## ☀️ Solana (SOL) Intelligence")
    st.markdown("Real-time market data combined with XGBoost AI predictions.")
    st.divider()

    # --- 1. Top Level Metrics ---
    # Fetch Data
    with st.spinner("Fetching live market data..."):
        df = fetch_kraken_data("SOLUSD", interval=1440)

    if not df.empty:
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # Calculations
        price = latest['close']
        change = price - prev['close']
        pct_change = (change / prev['close']) * 100
        vol = latest['volume']
        
        # Native Streamlit Metrics (Looks much better than dataframe)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Current Price", f"${price:,.2f}", f"{pct_change:+.2f}%")
        m2.metric("24h High", f"${latest['high']:,.2f}")
        m3.metric("24h Low", f"${latest['low']:,.2f}")
        m4.metric("Volume (24h)", f"{vol:,.0f}")
        
        # --- 2. Interactive Chart (Now with Volume) ---
        st.subheader("Price History & Trend")
        
        # Create a figure with secondary y-axis logic (for Volume)
        fig = go.Figure()
        
        # 2.1. Candlestick (Main Price)
        fig.add_trace(go.Candlestick(
            x=df['date'],
            open=df['open'], high=df['high'],
            low=df['low'], close=df['close'],
            name='OHLC'
        ))
        
        # 2.2. SMA 30 (Trend Line)
        sma30 = df['close'].rolling(30).mean()
        fig.add_trace(go.Scatter(
            x=df['date'], y=sma30, 
            mode='lines', name='SMA (30D)',
            line=dict(color='#FFA500', width=2)
        ))

        # 2.3. Volume Bars (Overlay at Bottom)
        # We use a transparent gray so it doesn't distract
        fig.add_trace(go.Bar(
            x=df['date'], y=df['volume'],
            name='Volume',
            marker_color='rgba(255, 255, 255, 0.2)', # Faint white
            yaxis='y2' 
        ))
        
        # Update Layout to handle the two axis
        fig.update_layout(
            height=500,
            xaxis_rangeslider_visible=False,
            template="plotly_dark",
            margin=dict(l=0, r=0, t=10, b=0),
            legend=dict(orientation="h", y=1, x=0),
            # Y-Axis 1 (Price)
            yaxis=dict(
                title="Price (USD)",
                side="left"
            ),
            # Y-Axis 2 (Volume) - Hidden scale, pushed to bottom
            yaxis2=dict(
                title="Volume",
                overlaying="y",
                side="right",
                showgrid=False,
                # The range multiplier (max * 4) pushes bars to the bottom 25% of chart
                range=[0, df['volume'].max() * 4] 
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("⚠️ Unable to load market data. Please try again later.")

    st.divider()

    # --- 3. AI Prediction Section ---
    st.subheader("🤖 AI Price Prediction")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.info(
            """
            **Model:** XGBoost Regressor  
            **Target:** Next Day High ($t+1$)  
            **Features:** RSI, SMA, Volatility, Lags  
            """
        )
        
        if st.button("🔮 Predict Tomorrow's High", type="primary", use_container_width=True):
            with st.spinner("Analyzing market patterns..."):
                try:
                    resp = requests.get(f"{API_URL}/predict/solana", timeout=8)
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state['pred_result'] = data
                    else:
                        st.error(f"API Error: {resp.status_code}")
                except Exception as e:
                    st.error(f"Connection Failed: {e}")

    with c2:
        # Display Result if available
        if 'pred_result' in st.session_state:
            res = st.session_state['pred_result']
            price = res['predicted_high']
            date = res['prediction_date']
            
            # Big Result Card
            st.success(f"### Prediction for {date}")
            st.metric(label="Predicted High Price", value=f"${price:,.2f}")
            
            # Simple Analysis
            if not df.empty:
                current_high = df.iloc[-1]['high']
                diff = price - current_high
                if diff > 0:
                    st.caption(f"🚀 Bullish: Predicted to be **${diff:.2f} higher** than today's high.")
                else:
                    st.caption(f"🔻 Bearish: Predicted to be **${abs(diff):.2f} lower** than today's high.")