import yfinance as yf
import smtplib
import datetime
import pandas as pd

# Replace with your email credentials
sender_email = "your_email@example.com"
sender_password = "your_password"
receiver_email = "your_email@example.com"

def check_voo_price():
    # Get the current price of VOO
    voo = yf.Ticker("VOO")
    current_price = voo.history(period="1d")["Close"][0]

    # Get the average price for the past month
    past_month = datetime.datetime.now() - datetime.timedelta(days=30)
    past_month_data = voo.history(start=past_month, end=datetime.datetime.now())
    past_month_avg = past_month_data["Close"].mean()

    # Calculate the percentage difference
    percentage_difference = (current_price / past_month_avg - 1) * 100

    # Check if the price is less than 15% of the past month average
    if percentage_difference < -15:
        # Send an email alert
        subject = "VOO Price Alert"
        body = f"The current price of VOO is {current_price}, which is {percentage_difference:.2f}% below the past month average of {past_month_avg}. This is a good time to buy!"

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, f"Subject: {subject}\n\n{body}")

        print("Email sent successfully!")
    else:
        print("VOO price is not currently below 15% of the past month average.")

if __name__ == "__main__":
    check_voo_price()