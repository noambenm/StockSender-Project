# streamlit_app.py

import streamlit as st
import requests
import re

# ==========================
# Configuration
# ==========================
API_GATEWAY_URL = "https://mycuudb69d.execute-api.us-east-1.amazonaws.com/V1/subscribe"

# ==========================
# Page Configuration
# ==========================
st.set_page_config(
    page_title="Stock Sender TM",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ==========================
# Title and Description
# ==========================
st.title("📈 Stock Sender TM")
st.divider()
st.subheader("Subscribe to Daily Stock Updates")

st.markdown(
    """
    Enter your email address and the stock ticker you wish to monitor.
    We'll send you daily updates based on your chosen ticker.
    """
)

# ==========================
# Form Handling
# ==========================
with st.form(key='subscription_form'):
    # User Inputs
    user_email = st.text_input(
        label="✉️ Email Address",
        placeholder="your.email@example.com",
        help="Please enter a valid email address."
    )
    
    chosen_ticker = st.text_input(
        label="📊 Stock Ticker",
        value="VOO",
        max_chars=5,
        help="Please enter a valid stock ticker symbol (e.g., AAPL, GOOGL)."
    )
    
    # Submit Button
    submit_button = st.form_submit_button(label="Submit", type="primary")

# ==========================
# Handle Form Submission
# ==========================
if submit_button:
    # ==========================
    # Input Validation
    # ==========================
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    ticker_pattern = r'^[A-Za-z0-9]{1,5}$'
    
    is_valid_email = re.match(email_pattern, user_email)
    is_valid_ticker = re.match(ticker_pattern, chosen_ticker.upper())
    
    if not user_email or not chosen_ticker:
        st.error("🔴 Both email and ticker fields are required.")
    elif not is_valid_email:
        st.error("🔴 Please enter a valid email address.")
    elif not is_valid_ticker:
        st.error("🔴 Please enter a valid ticker symbol (1-5 alphanumeric characters).")
    else:
        # ==========================
        # Prepare Payload
        # ==========================
        payload = {
            "user_email": user_email,
            "chosen_ticker": chosen_ticker.upper()
        }
        
        # ==========================
        # Send POST Request
        # ==========================
        try:
            response = requests.post(API_GATEWAY_URL, json=payload)
            
            if response.status_code == 200:
                st.success("✅ Subscription successful! You will receive daily updates shortly.")
            else:
                st.error(f"🔴 Failed to subscribe: {response.text}")
        
        except requests.exceptions.RequestException as e:
            st.error(f"🔴 An error occurred: {e}")
