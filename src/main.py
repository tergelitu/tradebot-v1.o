def rsi_signal(ticker='GC=F'):
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from mplfinance.original_flavor import candlestick_ohlc
    from datetime import datetime, timedelta
    from GoogleNews import GoogleNews
    from textblob import TextBlob
    import tweepy
    from colorama import Fore, Style, init
    import time
    import os
    from utils.data_processing import download_data, calculate_rsi, generate_signals
    from dotenv import load_dotenv

    load_dotenv()  # Load environment variables from .env file

    init(autoreset=True)

    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    if not bearer_token:
        raise ValueError("Bearer token not found. Please set the TWITTER_BEARER_TOKEN environment variable.")

    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=10)
    
    data = download_data(ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    data.reset_index(inplace=True)
    data = data[data['Datetime'].dt.weekday < 5]
    data['Continuous_Index'] = range(len(data))
    
    ohlc_data = data[['Continuous_Index', 'Open', 'High', 'Low', 'Close']].values
    
    def detect_asset_type(ticker):
        if '-' in ticker:
            return 'crypto'
        elif len(ticker) == 6 and ticker.isupper():
            return 'forex'
        else:
            return 'stock'

    def fetch_stock_news(ticker, asset_type):
        googlenews = GoogleNews(lang='en')
        if asset_type == 'crypto':
            googlenews.search(f"{ticker} cryptocurrency news")
        elif asset_type == 'forex':
            googlenews.search(f"{ticker} forex news")
        else:
            googlenews.search(f"{ticker} stock news")
        news_list = googlenews.get_texts()
        return news_list

    def fetch_social_media_trends(ticker):
        query = f"{ticker} -is:retweet lang:en"
        tweets = []
        try:
            for tweet in tweepy.Paginator(client.search_recent_tweets, query=query, tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=100):
                tweets.append(tweet.text)
        except tweepy.TooManyRequests:
            print("Rate limit exceeded. Waiting for 15 minutes before retrying...")
            time.sleep(15 * 60)  # wait for 15 minutes
            return fetch_social_media_trends(ticker)  # retry fetching tweets
        return tweets

    def analyze_sentiment(text_list):
        sentiment_scores = []
        for text in text_list:
            analysis = TextBlob(text)
            if analysis.sentiment.polarity > 0:
                sentiment_scores.append('Positive')
            elif analysis.sentiment.polarity == 0:
                sentiment_scores.append('Neutral')
            else:
                sentiment_scores.append('Negative')
        return sentiment_scores

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, figsize=(12, 16), gridspec_kw={'height_ratios': [3, 1, 1, 1]}, facecolor='black')
    ax1.set_facecolor('black')
    
    candlestick_ohlc(ax1, ohlc_data, width=0.6, colorup='white', colordown='blue')
    
    ax1.xaxis.set_major_locator(plt.MaxNLocator(10))  
    def format_date(x, _):
        if x < 0 or x >= len(data):
            return ''
        return data['Datetime'].iloc[int(x)].strftime('%Y-%m-%d %H:%M')
    
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(format_date))
    plt.xticks(rotation=45, color='white')
    
    ax1.grid(True, color='gray')
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    
    data['RSI'] = calculate_rsi(data)
    data = generate_signals(data)

    ax2.set_facecolor('black')
    ax2.set_title('RSI', color='white')
    ax2.plot(data['Continuous_Index'], data['RSI'], color='white')
    ax2.axhline(80, color='red', linestyle='--')
    ax2.axhline(20, color='green', linestyle='--')
    ax2.grid(True, color='gray')
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')
    
    ax1.plot(data.loc[data['buy_signal'], 'Continuous_Index'], data.loc[data['buy_signal'], 'Close'], '^', markersize=10, color='green', label='Buy Signal')
    ax1.plot(data.loc[data['sell_signal'], 'Continuous_Index'], data.loc[data['sell_signal'], 'Close'], 'v', markersize=10, color='red', label='Sell Signal')
    ax1.legend()

    asset_type = detect_asset_type(ticker)
    print(f"Fetching news for {ticker} ({asset_type})")
    news_list = fetch_stock_news(ticker, asset_type)
    sentiment_scores = analyze_sentiment(news_list)

    sentiment_colors = {'Positive': 'green', 'Neutral': 'grey', 'Negative': 'red'}
    for i, (news, sentiment) in enumerate(zip(news_list, sentiment_scores)):
        ax3.plot(i, 1, 'o', color=sentiment_colors[sentiment], markersize=10)

    ax3.set_yticks([])
    ax3.set_title('News Sentiment', color='white')
    ax3.grid(True, color='gray')
    ax3.tick_params(axis='x', colors='white')
    ax3.tick_params(axis='y', colors='white')

    print(f"Fetching social media trends for {ticker}")
    social_media_list = fetch_social_media_trends(ticker)
    social_media_sentiment_scores = analyze_sentiment(social_media_list)

    for i, (tweet, sentiment) in enumerate(zip(social_media_list, social_media_sentiment_scores)):
        ax4.plot(i, 1, 'o', color=sentiment_colors[sentiment], markersize=10)

    ax4.set_yticks([])
    ax4.set_title('Social Media Sentiment', color='white')
    ax4.grid(True, color='gray')
    ax4.tick_params(axis='x', colors='white')
    ax4.tick_params(axis='y', colors='white')

    plt.tight_layout()
    plt.show()

    for news, sentiment in zip(news_list[:10], sentiment_scores[:10]):
        print(f"{Fore.YELLOW}News: {Style.RESET_ALL}{news} \n{Fore.CYAN}Sentiment: {sentiment}\n")
    
    for tweet, sentiment in zip(social_media_list[:10], social_media_sentiment_scores[:10]):
        print(f"{Fore.YELLOW}Tweet: {Style.RESET_ALL}{tweet} \n{Fore.CYAN}Sentiment: {sentiment}\n")

def main():
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else 'GC=F'
    rsi_signal(ticker)

if __name__ == "__main__":
    main()