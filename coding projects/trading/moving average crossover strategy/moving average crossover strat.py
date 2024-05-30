import pandas as pd
import numpy as np
import yfinance as yf

# Parameters
short_window = 50
long_window = 200

# Fetch historical data
symbol = 'AAPL'  # Example stock symbol
data = yf.download(symbol, start='2020-01-01', end='2024-05-29')

# Calculate moving averages
data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

# Generate signals
data['Signal'] = 0.0
data['Signal'][short_window:] = np.where(data['Short_MA'][short_window:] > data['Long_MA'][short_window:], 1.0, 0.0)
data['Position'] = data['Signal'].diff()

# Display signals
print(data[['Close', 'Short_MA', 'Long_MA', 'Signal', 'Position']])

# Backtesting
initial_capital = 100000.0
positions = pd.DataFrame(index=data.index).fillna(0.0)
positions[symbol] = 100 * data['Signal']
portfolio = positions.multiply(data['Close'], axis=0)
pos_diff = positions.diff()

# Calculate portfolio value
portfolio['holdings'] = (positions.multiply(data['Close'], axis=0)).sum(axis=1)
portfolio['cash'] = initial_capital - (pos_diff.multiply(data['Close'], axis=0)).sum(axis=1).cumsum()
portfolio['total'] = portfolio['cash'] + portfolio['holdings']

# Plot results
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['Short_MA'], label='50-Day MA')
plt.plot(data['Long_MA'], label='200-Day MA')
plt.plot(data.loc[data['Position'] == 1.0].index, data['Short_MA'][data['Position'] == 1.0], '^', markersize=10, color='g', lw=0, label='Buy Signal')
plt.plot(data.loc[data['Position'] == -1.0].index, data['Short_MA'][data['Position'] == -1.0], 'v', markersize=10, color='r', lw=0, label='Sell Signal')
plt.title(f'{symbol} Price with Buy and Sell Signals')
plt.legend()
plt.show()

# Portfolio value plot
plt.figure(figsize=(12, 8))
plt.plot(portfolio['total'], label='Portfolio Value')
plt.title('Portfolio Value Over Time')
plt.legend()
plt.show()