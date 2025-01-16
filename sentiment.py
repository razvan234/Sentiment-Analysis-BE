import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('all')


def sentiment_scores(sentence):
    from nltk.sentiment import SentimentIntensityAnalyzer

    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)

    if sentiment_dict['compound'] >= 0.05:
        return "Positive"
    elif sentiment_dict['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"


def sentiment_summary(comments):
    summary = {"positive": 0, "neutral": 0, "negative": 0}

    for comment in comments:
        if comment.sentiment == "Positive":
            summary["positive"] += 1
        elif comment.sentiment == "Negative":
            summary["negative"] += 1
        else:
            summary["neutral"] += 1

    total = summary["positive"] + summary["neutral"] + summary["negative"]
    if summary["positive"] / total > 0.6:
        overall_sentiment = "Mostly Positive"
    elif summary["negative"] / total > 0.6:
        overall_sentiment = "Mostly Negative"
    else:
        overall_sentiment = "Mixed"

    return {
        "summary": summary,
        "overall_sentiment": overall_sentiment
    }
