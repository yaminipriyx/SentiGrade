import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize the sentiment intensity analyzer
sia = SentimentIntensityAnalyzer()

# Function to analyze sentiment
def analyze_sentiment(comment):
    sentiment_scores = sia.polarity_scores(comment)
    if sentiment_scores['compound'] >= 0.05:
        return "Positive"
    elif sentiment_scores['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Input comments for analysis
while True:
    comment = input("Enter a comment (or type 'exit' to quit): ")
    if comment.lower() == 'exit':
        break
    sentiment = analyze_sentiment(comment)
    print(f"The sentiment of the comment is: {sentiment}")
    print(f"The score of the comment is: {sia.polarity_scores(comment)}")