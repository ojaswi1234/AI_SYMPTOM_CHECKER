import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

AI_API_KEY = os.getenv('GPT_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)