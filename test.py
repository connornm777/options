import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Collect options data for AAPL
ticker_symbol = "TSLA"
ticker = yf.Ticker(ticker_symbol)

# Get the list of available expiration dates
available_dates = ticker.options

# Choose the first expiration date for demonstration (you can choose any other)
chosen_expiry = available_dates[0]

options_data = ticker.option_chain(date=chosen_expiry)
calls = options_data.calls
puts = options_data.puts

# Merge calls and puts data on 'strike' column
merged = pd.merge(calls, puts, on='strike', suffixes=('_call', '_put'))

# Store the value (last trade price) and strike price
df = merged[['strike', 'lastPrice_call', 'volume_call']]

# Ensure the dataframe is sorted by strike price
df = df.sort_values(by='strike')

# Compute the unsmoothed second derivative
second_derivative = np.gradient(np.gradient(df['lastPrice_call'].to_numpy(), df['strike'].to_numpy()), df['strike'].to_numpy())

# Normalize the volume weights to sum to one
normalized_weights = df['volume_call'] / df['volume_call'].sum()

# Weight the second derivative by the normalized volume weights
normalized_weighted_derivative = second_derivative * normalized_weights.to_numpy()

# Plot
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot the unsmoothed second derivative
ax1.plot(df['strike'], second_derivative, label='Unsmoothed 2nd Derivative', color='blue')
ax1.plot(df['strike'], normalized_weighted_derivative, label='Normalized Weighted 2nd Derivative', color='orange', linestyle='--')
ax1.set_xlabel('Strike Price')
ax1.set_ylabel('Derivative Value')
ax1.legend(loc='upper left')

# Create a second y-axis for volume
ax2 = ax1.twinx()
ax2.plot(merged['strike'], merged['volume_call'], label='Volume (Calls)', color='green', alpha=0.5)
ax2.set_ylabel('Volume')
ax2.legend(loc='upper right')

plt.title(f'Second Derivative (Unsmoothed & Normalized Weighted) and Volume for {ticker_symbol} Calls (Expiry: {chosen_expiry})')
plt.grid(True)
plt.show()
