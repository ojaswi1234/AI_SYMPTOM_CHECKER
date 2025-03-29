const express = require('express');
const bodyParser = require('body-parser');
const dotenv = require('dotenv');
const fetch = require('node-fetch');

dotenv.config();

const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.json());
app.use(express.static('static'));

// Environment variables
const DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions";
const API_KEY = process.env.DEEPSEEK_API_KEY;

// Helper function to make API requests
async function makeApiRequest(url, payload, headers) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(payload)
        });
        if (!response.ok) {
            throw new Error('Failed to fetch response from DeepSeek API');
        }
        return await response.json();
    } catch (error) {
        throw error;
    }
}

// Routes
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/templates/index.html');
});

app.post('/get_response', async (req, res) => {
    const userInput = req.body.user_input;
    if (!userInput) {
        return res.status(400).json({ error: 'No input provided' });
    }

    const headers = { 'Authorization': `Bearer ${API_KEY}`, 'Content-Type': 'application/json' };
    const payload = { query: userInput };

    try {
        const response = await makeApiRequest(DEEPSEEK_API_URL, payload, headers);
        res.json(response);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch response from DeepSeek API' });
    }
});

app.post('/symptom_check', (req, res) => {
    const symptoms = req.body.symptoms;
    if (!symptoms) {
        return res.status(400).json({ error: 'No symptoms provided' });
    }

    const possibleDiagnosis = `Based on the symptoms, the possible diagnosis is`;
    res.json({ result: possibleDiagnosis });
});

// Start server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
