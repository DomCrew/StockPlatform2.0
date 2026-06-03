"""Module for sentiment analysis of finance articles"""
from transformers import (
    AutoConfig,
    AutoModelForSequenceClassification,
    AutoTokenizer,
    pipeline,
)

MODEL_ID = "ProsusAI/finbert"
_sentiment_analyzer = None


def _get_sentiment_analyzer():
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        config = AutoConfig.from_pretrained(MODEL_ID)
        model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_ID,
            config=config,
        )

        _sentiment_analyzer = pipeline(
            "text-classification",
            model=model,
            tokenizer=tokenizer,
            truncation=True,
            batch_size=16,
        )
    return _sentiment_analyzer


def get_news_and_sentiment(news: list):
    """Returns latest news and their sentiment for a given ticker."""
    titles = [f"{article['title']}. {article['summary']}" for article in news]
    sentiment_analyzer = _get_sentiment_analyzer()
    sentiments = sentiment_analyzer(titles)

    for article, sentiment in zip(news, sentiments):
        article["sa_label"] = sentiment["label"]
        article["sa_score"] = sentiment["score"]

    return news


if __name__ == "__main__":
    print(get_news_and_sentiment([{"title": "Test title", "summary": "Test summary."}]))
