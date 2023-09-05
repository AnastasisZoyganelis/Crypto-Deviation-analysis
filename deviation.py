import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

chainlink_url = 'https://api.coingecko.com/api/v3/coins/fetch-ai/market_chart'
chainlink_params = {'vs_currency': 'usd', 'days': '365', 'interval': 'daily'}
chainlink_response = requests.get(chainlink_url, params=chainlink_params)


if chainlink_response.status_code == 200:
    chainlink_data = chainlink_response.json()

    # Extract the closing prices from the chart data
    prices = chainlink_data['prices']

    df = pd.DataFrame(prices, columns=['timestamp', 'price'])

    # Convert the 'timestamp' column to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Calculate the percentage change in price
    df['price_change_percent'] = df['price'].pct_change() * 100

    # Drop the last row with NaN values
    df = df.dropna()

    # Calculate the mean and standard deviation of price change
    mean_price_change = df['price'].mean()
    std_dev_price_change = df['price'].std()

    # Specify the range (e.g., 1 standard deviation)
    num_std_devs = 1

    # Calculate the deviation range
    lower_bound = mean_price_change - (num_std_devs * std_dev_price_change)
    upper_bound = mean_price_change + (num_std_devs * std_dev_price_change)
    outofdev = df[df['price'] < lower_bound]['price']
    overofdev = df[df['price'] > upper_bound]['price']
    insidedev = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)]['price']

   
    plt.figure(figsize=(12, 6))
    tick_step = 0.05
    plt.xlim(0,0.55)
    plt.xticks(np.arange(0, 0.55 + tick_step, tick_step))

    # Separate positive and negative changes
    

    # Create histograms for positive and negative changes with different colors
    plt.hist(overofdev, bins=100, edgecolor='black', color='green', alpha=0.5, label='OVER DEV ')
    plt.hist(insidedev, bins=100, edgecolor='black', color='blue', alpha=0.5, label='UNDER DEV ')
    plt.hist(outofdev, bins=100, edgecolor='black', color='red', alpha=0.5, label='INSIDE RANGE ')

    # Plot vertical lines for the deviation range
    plt.axvline(lower_bound, color='red', linestyle='--', label='Lower Deviation Bound')
    plt.axvline(upper_bound, color='blue', linestyle='--', label='Upper Deviation Bound')
    plt.axvline(mean_price_change,color='yellow',linestyle='--', label='MEAN')

    plt.xlabel('Price ')
    plt.ylabel('Frequency')
    plt.title('FET Price Histogram Over 365 Days with Deviation Range')
    plt.grid(axis='y', alpha=0.75)
    plt.legend()
    plt.tight_layout()
    plt.show()
else:
    print('Failed to retrieve data. Status code:', chainlink_response.status_code)
