import requests
import matplotlib.pyplot as plt
import pandas as pd
import hmac
import hashlib
import time

# Step 1: Getting real-time cryptocurrency prices from KuCoin
def get_kucoin_price(symbol):
    url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    return data['data']['price']

# Step 2: Plotting price history
def plot_price_history(prices, crypto_name):
    plt.figure(figsize=(10, 5))
    plt.plot(prices, label=crypto_name)
    plt.xlabel('Time')
    plt.ylabel('Price in USD')
    plt.title(f'{crypto_name} Price History')
    plt.legend()
    plt.grid(True)
    plt.show()

# Step 3: Managing a cryptocurrency portfolio
def create_portfolio():
    portfolio = pd.DataFrame(columns=['Crypto', 'Amount', 'Price per Unit (USD)', 'Total Value (USD)'])
    return portfolio

def add_to_portfolio(portfolio, crypto, amount, price):
    total_value = amount * price
    portfolio = portfolio.append({'Crypto': crypto, 'Amount': amount, 'Price per Unit (USD)': price, 'Total Value (USD)': total_value}, ignore_index=True)
    return portfolio

# Step 4: Executing automated trades on KuCoin
def kucoin_api_request(api_key, api_secret, api_passphrase, method, endpoint, data=None):
    url = f"https://api.kucoin.com{endpoint}"
    now = int(time.time() * 1000)
    str_to_sign = str(now) + method + endpoint
    if data:
        str_to_sign += str(data)
    
    signature = hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
    headers = {
        "KC-API-KEY": api_key,
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-PASSPHRASE": api_passphrase,
        "Content-Type": "application/json"
    }
    
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, json=data, headers=headers)
    
    return response.json()

def execute_trade(api_key, api_secret, api_passphrase, symbol, size, side='buy'):
    endpoint = "/api/v1/orders"
    order = {
        "clientOid": str(int(time.time() * 1000)),
        "side": side,
        "symbol": symbol,
        "type": "market",
        "size": size
    }
    
    response = kucoin_api_request(api_key, api_secret, api_passphrase, "POST", endpoint, order)
    return response

# Example usage
if __name__ == "__main__":
    # Get real-time price from KuCoin
    symbol = 'BTC-USDT'
    price = get_kucoin_price(symbol)
    print(f"The current price of Bitcoin is: ${price}")

    # Plot price history
    prices = [get_kucoin_price(symbol) for _ in range(10)]  # Simulated data for the sake of example
    plot_price_history(prices, 'Bitcoin')

    # Manage portfolio
    portfolio = create_portfolio()
    portfolio = add_to_portfolio(portfolio, 'Bitcoin', 0.1, float(price))
    print(portfolio)

    # Execute a trade (uncomment and fill in your KuCoin API keys to execute)
    # api_key = 'your_api_key'
    # api_secret = 'your_api_secret'
    # api_passphrase = 'your_api_passphrase'
    # order = execute_trade(api_key, api_secret, api_passphrase, 'BTC-USDT', '0.001', 'buy')
    # print(order)
