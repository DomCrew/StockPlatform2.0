from transformers import pipeline

from collection.finance import get_news

def get_news_and_sentiment(ticker: str, count: int):
    """ Returns latest news and their sentiment for a given ticker """
    news = get_news(ticker, count)
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
