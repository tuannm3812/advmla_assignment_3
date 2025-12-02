# app/main.py
import streamlit as st

# Page Configuration (Must be first)
st.set_page_config(
    page_title="Crypto Investment Dashboard",
    page_icon="📈",
    layout="wide"
)

# Import Student Components
# Note: Ensure an empty __init__.py exists in app/students/
from students.sol_25739083 import render_solana_tab

def main():
    st.title("💰 Cryptocurrency Investment Dashboard")
    st.markdown("Select a cryptocurrency to view historical data and AI-powered price predictions.")
    
    # Create Tabs
    # You can add placeholders for group members here
    tab_sol, tab_btc, tab_eth, tab_xrp = st.tabs([
        "☀️ Solana (SOL)", 
        "₿ Bitcoin (BTC)", 
        "⟠ Ethereum (ETH)", 
        "✕ Ripple (XRP)"
    ])
    
    # --- Tab 1: YOUR WORK (Solana) ---
    with tab_sol:
        render_solana_tab()
        
    # --- Other Tabs (Placeholders) ---
    with tab_btc:
        st.info("Bitcoin module not loaded in individual view.")
        
    with tab_eth:
        st.info("Ethereum module not loaded in individual view.")
        
    with tab_xrp:
        st.info("Ripple module not loaded in individual view.")

    # Footer
    st.divider()
    st.caption("AT3 - Data Product with Machine Learning | Group 10")

if __name__ == "__main__":
    main()