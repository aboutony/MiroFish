import os
import requests
from typing import Dict, List

# API Keys retrieved from your .env file
# Defaults to 'demo' or 'placeholder' if not found
ALPHA_VANTAGE_KEY = os.getenv("MARKET_DATA_API_KEY", "demo")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "placeholder")

def fetch_stock_quote(symbol: str) -> Dict:
    """
    Fetches real-time price data for a specific stock ticker.
    This provides the 'hard data' for our trading agents.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        quote = data.get("Global Quote", {})
        
        # Structure the data for easy consumption by the simulation engine
        return {
            "symbol": quote.get("01. symbol", symbol),
            "price": quote.get("05. price", "0.00"),
            "change_percent": quote.get("10. change percent", "0%"),
            "volume": quote.get("06. volume", "0"),
            "timestamp": quote.get("07. latest trading day", "N/A")
        }
    except Exception as e:
        return {"error": str(e), "symbol": symbol, "price": "Data Unavailable"}

def fetch_market_news(symbol: str) -> List[str]:
    """
    Fetches recent news headlines related to the stock.
    This provides the 'soft data' for sentiment analysis.
    """
    if NEWS_API_KEY == "placeholder":
        return [f"General market sentiment remains cautious for {symbol}."]
    
    url = f"https://newsapi.org/v2/everything?q={symbol}&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        articles = response.json().get("articles", [])
        return [a['title'] for a in articles]
    except:
        return [f"Could not retrieve news for {symbol} at this time."]

def prepare_simulation_seed(symbol: str) -> str:
    """
    Combines price and news into a high-density string.
    This acts as the 'Seed' that forces the swarm of agents to react.
    """
    quote = fetch_stock_quote(symbol)
    news = fetch_market_news(symbol)
    
    seed_report = f"MARKET UPDATE for {symbol}: "
    seed_report += f"The current trading price is ${quote['price']} ({quote['change_percent']} change). "
    seed_report += f"Recent key developments: {' | '.join(news)}"
    
    return seed_report
