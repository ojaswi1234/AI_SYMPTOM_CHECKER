from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check_symptoms', methods=['POST'])
def check_symptoms():
 
    symptoms = request.form['symptoms']

    if not symptoms.strip():
        prompt = "No symptoms provided."
    else:
        prompt = f"""
       You are a medical AI that analyzes symptoms to suggest possible conditions, ordered by likelihood. If input is vague or invalid, respond: 'Please provide specific symptoms for accurate assessment.' Otherwise, list numbered possibilities (e.g., '1. Condition X – Brief advice; 2. Condition Y – Brief advice'). Use phrases like 'may suggest' or 'could indicate,' avoid disclaimers, and keep advice actionable (e.g., 'Rest if fatigued; see a doctor for persistent fever'). Never diagnose definitively. Example: '1. Dehydration – Drink fluids; 2. Migraine – Avoid triggers.' Respond only to health-related queries. Symptoms Provided: {symptoms}
        """

    try:
        response = model.generate_content(prompt)
        ai_response = response.text  

        return jsonify({'result': ai_response})

    except Exception as e:
        print(f"Error communicating with Gemini API: {e}")
        return jsonify({'error': str(e)}), 500  


if __name__ == '__main__':
    app.run(debug=True) 

