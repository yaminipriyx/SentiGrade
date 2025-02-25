from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
from googletrans import Translator, constants
from datetime import datetime

app = Flask(__name__)

# Initialize Translator
translator = Translator()

# Access the dictionary of language codes to full names
language_map = constants.LANGUAGES

# Function to get full language name from the code
def get_language_name(language_code):
    return language_map.get(language_code, language_code)

# Pre-load some previous comments with sentiment and language info
previous_comments = [
    {
        'comment': '오늘 날씨가 좋지 않다',  # "The weather is not good today" in Korean
        'translated_comment': translator.translate('오늘 날씨가 좋지 않다', dest='en').text,
        'sentiment': 'Neutral',
        'language': get_language_name(translator.detect('오늘 날씨가 좋지 않다').lang),
        'timestamp': '2024-11-22 12:10:00'
    },
    {
        'comment': '昨日は良い日だった',  # "Yesterday was a good day" in Japanese
        'translated_comment': translator.translate('昨日は良い日だった', dest='en').text,
        'sentiment': 'Negative',
        'language': get_language_name(translator.detect('昨日は良い日だった').lang),
        'timestamp': '2024-11-22 11:45:00'
    },
    {
        'comment': 'The product quality was decent, nothing special.',
        'translated_comment': 'The product quality was decent, nothing special.',
        'sentiment': 'Neutral',
        'language': get_language_name(translator.detect('The product quality was decent, nothing special.').lang),
        'timestamp': '2024-11-22 11:20:00'
    },
    {
        'comment': 'Absolutely fantastic experience!',
        'translated_comment': 'Absolutely fantastic experience!',
        'sentiment': 'Positive',
        'language': get_language_name(translator.detect('Absolutely fantastic experience!').lang),
        'timestamp': '2024-11-22 10:55:00'
    },
    {
        'comment': 'Das Essen war wirklich schlecht',  # "The food was really bad" in German
        'translated_comment': translator.translate('Das Essen war wirklich schlecht', dest='en').text,
        'sentiment': 'Negative',
        'language': get_language_name(translator.detect('Das Essen war wirklich schlecht').lang),
        'timestamp': '2024-11-22 10:30:00'
    }
]

@app.route('/', methods=['GET', 'POST'])
def index():
    comment = None
    sentiment = None

    if request.method == 'POST':
        # Get the input comment
        comment = request.form['comment']

        # Detect and translate comment to English
        detected_language_code = translator.detect(comment).lang
        detected_language = get_language_name(detected_language_code)
        translation = translator.translate(comment, dest='en')
        translated_comment = translation.text

        # Perform sentiment analysis on the translated comment
        analysis = TextBlob(translated_comment)
        polarity = analysis.sentiment.polarity

        # Determine the sentiment
        if polarity > 0:
            sentiment = 'Positive'
        elif polarity < 0:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'

        # Save the original comment, its sentiment, the language, and the timestamp
        previous_comments.append({
            'comment': comment,
            'translated_comment': translated_comment,
            'sentiment': sentiment,
            'language': detected_language,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return render_template('index.html', comment=comment, sentiment=sentiment, previous_comments=previous_comments)

@app.route('/sentiment-data')
def sentiment_data():
    # Collect sentiment statistics
    sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    for entry in previous_comments:
        sentiment_counts[entry['sentiment']] += 1
    return jsonify(sentiment_counts)

if __name__ == '__main__':
    app.run(debug=True)
