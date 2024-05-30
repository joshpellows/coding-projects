import pandas as pd
import numpy as np
import yfinance as yf

# Fetch historical data
symbol = 'AAPL'  # Example stock symbol
data = yf.download(symbol, start='2020-01-01', end='2024-05-29')

# Calculate RSI
def compute_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

data['RSI'] = compute_rsi(data)

# Generate signals
data['Signal'] = 0
data['Signal'][data['RSI'] < 30] = 1  # Buy signal
data['Signal'][data['RSI'] > 70] = -1  # Sell signal
data['Position'] = data['Signal'].shift()

# Backtesting
initial_capital = 100000.0
positions = pd.DataFrame(index=data.index).fillna(0.0)
positions[symbol] = 100 * data['Position']
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
plt.plot(data['RSI'], label='RSI', alpha=0.3)
plt.axhline(y=30, color='red', linestyle='--', alpha=0.5)
plt.axhline(y=70, color='green', linestyle='--', alpha=0.5)
plt.plot(data.loc[data['Signal'] == 1.0].index, data['Close'][data['Signal'] == 1.0], '^', markersize=10, color='g', lw=0, label='Buy Signal')
plt.plot(data.loc[data['Signal'] == -1.0].index, data['Close'][data['Signal'] == -1.0], 'v', markersize=10, color='r', lw=0, label='Sell Signal')
plt.title(f'{symbol} Price with Buy and Sell Signals')
plt.legend()
plt.show()

# Portfolio value plot
plt.figure(figsize=(12, 8))
plt.plot(portfolio['total'], label='Portfolio Value')
plt.title('Portfolio Value Over Time')
plt.legend()
plt.show()