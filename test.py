import yfinance as yf
import pandas as pd
voo = yf.Ticker("VOO")
voo_history = voo.history(period="1mo")
most_recent_open = voo_history.iloc[-1]['Open']
average_open = voo_history['Open'].mean()
print (voo_history)
print (most_recent_open)
print (average_open)
if most_recent_open < average_open * 0.85:
    print ("Buy VOO")
else:
    print ("Do not buy VOO")