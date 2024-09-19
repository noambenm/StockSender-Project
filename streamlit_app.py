import streamlit as st
import requests

st.title("Stock Sender TM")
st.divider()

st.subheader("Hello dear user")

user_email = st.text_input("Please enter your email address", help = "Please enter a valid email address")

chosen_ticker = st.text_input("Please enter a ticker", "VOO",help = "Please enter a valid ticker")

if st.button("Submit"):
    st.write(f"Please make sure the entered info is correct\nYour email addres: {user_email}\n Your chousen ticker: {chosen_ticker}")        
    st.write("Submit?")
    if st.button("Yes"):
        st.write("Thank you for your submission!")
        response = requests.post('https://mycuudb69d.execute-api.us-east-1.amazonaws.com/', json={"user_email": user_email,"chosen_ticker": chosen_ticker})
        print(response.status_code, response.text)

