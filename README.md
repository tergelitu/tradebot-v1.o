# Financial Instrument RSI Analysis and Visualization Bot 📊

This project develops a bot to analyze and visualize price data of various financial instruments using the **Relative Strength Index (RSI)** indicator. The bot fetches financial data, processes it, and generates insightful plots and trade signals to assist in trading decisions. Additionally, it analyzes news sentiment and social media trends to provide a comprehensive view of market sentiment.

## What is RSI? 🤔

The **Relative Strength Index (RSI)** is a momentum oscillator that measures the speed and change of price movements. It ranges from 0 to 100 and is typically used to identify overbought or oversold conditions in a market.

## Features 🌟

- **RSI Calculation**: Calculate the RSI for the given financial instrument.
- **Trade Signals**: Generate buy and sell signals based on RSI thresholds.
- **News Sentiment Analysis**: Fetch and analyze news articles related to the financial instrument to gauge market sentiment.
- **Social Media Trend Analysis**: Fetch and analyze social media trends to understand public sentiment.

## Installation 🔧

To set up the project, follow these steps:

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd data-science-project
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the project root directory.
   - Add your Twitter API bearer token to the `.env` file:
     ```
     TWITTER_BEARER_TOKEN=your_bearer_token_here
     ```

## Usage 🚀

To run the project and visualize the data with RSI, news sentiment, and social media trends, execute the following command:
```sh
python src/main.py
```

## License 📜

This project is licensed under the MIT License. See the LICENSE file for more details.