from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime

app = Flask(__name__)
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")  

if not GOOGLE_API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable.")
if not GEOAPIFY_API_KEY:
    raise ValueError("Please set the GEOAPIFY_API_KEY environment variable.")

EMERGENCY_KEYWORDS = [
    "life threatening",
    "seek immediate medical attention",
    "call emergency services",
    "urgent medical care",
    "immediately seek medical advice",
    "consult a doctor",
]

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

@app.route('/')
def index():
    return render_template('index.html', geoapify_api_key=GEOAPIFY_API_KEY)

@app.route('/check_symptoms', methods=['POST'])
def check_symptoms():
    symptoms = request.form['symptoms']

    if not symptoms.strip():
        return jsonify({'error': 'No symptoms provided.'}), 400

    prompt = f"""
    You are a medical AI that analyzes symptoms to suggest possible conditions, ordered by likelihood. If input is vague or invalid, respond: 'Please provide specific symptoms for accurate assessment.' Otherwise, list numbered possibilities (e.g., '1. Condition X – Brief advice; 2. Condition Y – Brief advice'). Use phrases like 'may suggest' or 'could indicate,' avoid disclaimers, and keep advice actionable (e.g., 'Rest if fatigued; see a doctor for persistent fever'). Never diagnose definitively. Example: '1. Dehydration – Drink fluids; 2. Migraine – Avoid triggers.' Respond only to health-related queries. Symptoms Provided: {symptoms}
    """

    try:
        response = model.generate_content(prompt)
        ai_response = response.text

        is_emergency = any(keyword.lower() in ai_response.lower() for keyword in EMERGENCY_KEYWORDS)

        # Generate report data
        report_data = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'symptoms': symptoms,
            'conditions': ai_response,
            'emergency': "Yes" if is_emergency else "No"
        }

        return jsonify({
            'result': ai_response,
            'emergency': is_emergency,
            'report_data': report_data
        })

    except Exception as e:
        print(f"Error communicating with Gemini API: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)