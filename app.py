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
    """Renders the main page with the symptom checker form."""
    return render_template('index.html')


@app.route('/check_symptoms', methods=['POST'])
def check_symptoms():
    """
    Receives symptom input from the user, queries the Gemini API, and returns the response.
    """
    symptoms = request.form['symptoms']

    prompt = f"""
    You are a helpful AI assistant specializing in providing preliminary information about potential health conditions based on provided symptoms. 
    However, you are NOT a substitute for a medical professional. Always advise users to consult with a doctor for diagnosis and treatment.

    Based on the following symptoms: {symptoms}

    Provide potential causes (health conditions) that could be associated with the given symptoms. 
    Do not provide specific medical advice or prescribe treatments.
    also dont provide any disclaimers or warnings. Just provide the list of potential causes.
    and yes, you can use the internet to find the most relevant and up-to-date information.
    Please provide the response in a simple and clear format, such as a numbered list or bullet points.
    and classify the content
    and use only one * for headings
    and if the {symptoms} is empty, just say "No symptoms provided".
    and if the {symptoms} is invalid, just say "Invalid symptoms provided".
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

