def download_data(symbol, start_date, end_date, interval='15m'):
    import yfinance as yf
    data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
    return data

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def generate_signals(data):
    data['buy_signal'] = (data['RSI'] < 20) & (data['RSI'].shift(1) >= 20)
    data['sell_signal'] = (data['RSI'] > 80) & (data['RSI'].shift(1) <= 80)
    return data