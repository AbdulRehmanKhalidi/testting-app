import numpy as np
from flask import Flask, render_template, request, jsonify
import sqlite3

# from correction import correct
from without import find_closest_words
from prediction import predict_next_word
from utils import parese_sentence

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check')
def search():
    return render_template('second1.html')


@app.route('/keyboard')
def keyboard():
    return render_template("keyboard.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/correct', methods=['POST'])
def process():
    input_text = request.json.get('input_text', '')
    word_list = open('wordlist.txt', "r+", encoding="utf-8").read().split()
    incorrect_words = {}
    input_sentence = input_text.rstrip('.')
    sentence_endings = ['۔', '.', '!', '?']
    input_sentence = input_text.strip()
    for ending in sentence_endings:
        if input_sentence.endswith(ending):
            input_sentence = input_sentence[:-1]
    for word in input_sentence.split():
        if word not in word_list:
            suggestions = find_closest_words(word, word_list)
            if suggestions:
                incorrect_words[word] = suggestions
    return jsonify(incorrect_words)


# @app.route('/check', methods=['POST'])
# def check():
#     text = str(request.form["words"])
#     a = correct(text)
#     return jsonify({'text': a})

@app.route('/predict', methods=['POST'])
def predict():
    input_text = request.form['words']
    predicted_word = predict_next_word(input_text)
    response = jsonify({'text': predicted_word})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/guide', methods=['POST'])
def guide():
    if request.method == 'POST':
        input_sent = request.form['sentence']
        tags = parese_sentence(input_sent)
        return jsonify(tags)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
