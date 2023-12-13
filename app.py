from flask import Flask, render_template, request
from google.cloud import language

app = Flask(__name__)

# Set the path to your service account key JSON file
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service-account-key.json'

def analyze_sentiment(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    return sentiment.score, sentiment.magnitude

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    score, magnitude = analyze_sentiment(text)
    return render_template('result.html', text=text, score=score, magnitude=magnitude)

if __name__ == '__main__':
    app.run(debug=True)
