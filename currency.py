import yfinance as yf

# Define currency pair symbol (e.g., USD/ILS)
currency_pair = 'USDILS=X'

# Get historical data for the currency pair
ticker = yf.Ticker(currency_pair)
data = ticker.history(period='1d', interval='1m')  # Get today's minute data

# Extract the latest close price (exchange rate)
usd_price = round(data['Open'].iloc[-1], 2)
print(f"1 USD = {usd_price} ILS")
