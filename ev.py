import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Collect options data for AAPL
ticker_symbol = "NVDA"
ticker = yf.Ticker(ticker_symbol)

# Get the current price of AAPL
current_price = ticker.history(period="1d")['Close'][0]

# Get the list of available expiration dates
available_dates = ticker.options

# Choose the first expiration date for demonstration (you can choose any other)
chosen_expiry = available_dates[0]

options_data = ticker.option_chain(date=chosen_expiry)
calls = options_data.calls
puts = options_data.puts

# Merge calls and puts data on 'strike' column
merged = pd.merge(calls, puts, on='strike', suffixes=('_call', '_put'))

# Calculate the value: call - put + strike
merged['synthetic_forward'] = merged['lastPrice_call'] - merged['lastPrice_put'] + merged['strike']

# Plot
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot synthetic forward
ax1.plot(merged['strike'], merged['synthetic_forward'], label='Synthetic Forward', color='purple')
ax1.axhline(current_price, color='red', linestyle='--', label=f'Current Price: ${current_price:.2f}')
ax1.set_xlabel('Strike Price')
ax1.set_ylabel('Value')
ax1.legend(loc='upper left')

# Create a second y-axis for volume
ax2 = ax1.twinx()
ax2.plot(merged['strike'], merged['volume_call'], label='Volume (Calls)', color='blue', alpha=0.5)
ax2.set_ylabel('Volume')
ax2.legend(loc='upper right')

plt.title(f'Synthetic Forward and Volume for {ticker_symbol} (Expiry: {chosen_expiry})')
plt.grid(True)
plt.show()
