"""Module for sentiment analysis of finance articles"""
from transformers import pipeline

def get_news_and_sentiment(ticker: str, count: int, news: list):
    """ Returns latest news and their sentiment for a given ticker """
    titles = [f"{article["title"]}. {article["summary"]}" for article in news]
    sentiment_analyzer = pipeline(
        "text-classification",
        model="yiyanghkust/finbert-tone",
        truncation=True,
        batch_size=16
    )
    sentiments = sentiment_analyzer(titles)

    for article, sentiment in zip(news, sentiments):
        article["sa_label"] = sentiment["label"]
        article["sa_score"] = sentiment["score"]

    return news

if __name__ == "__main__":
    print(get_news_and_sentiment("AAPL", 5))
