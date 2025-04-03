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
        You are an AI assistant trained to provide preliminary insights into potential health conditions based on symptoms provided by users. 
        Your role is to analyze the symptoms and suggest possible causes in a concise and clear manner. 
        Ensure the response is formatted as a numbered list or bullet points, and classify the content under relevant headings.
       
        Symptoms provided: {symptoms}
        and use * only for heading and that too only one at the start of the response.
        and use numbers  only for bullet points.dont give any disclaimers or warnings.
        If the symptoms are invalid or nonsensical, respond with "Invalid symptoms provided."
        if the symptoms are empty, don't offer some general health advice
        just, respond with "No symptoms provided." 
        Otherwise, provide a list of potential causes based on the symptoms.
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

