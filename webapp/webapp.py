from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import requests
import sqlite3

app = Flask(__name__)
CORS(app)

def setup_database():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS conversation_history
                 (id INTEGER PRIMARY KEY, session_id TEXT, role TEXT, content TEXT)''')
    conn.commit()
    conn.close()

def add_message_to_db(session_id, role, content):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO conversation_history (session_id, role, content) VALUES (?, ?, ?)", (session_id, role, content))
    conn.commit()
    conn.close()

def get_conversation_history(session_id):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("SELECT role, content FROM conversation_history WHERE session_id = ?", (session_id,))
    messages = [{'role': role, 'content': content} for role, content in c.fetchall()]
    conn.close()
    return messages



# Function to send messages to the API and get responses
def chat_with_openai(api_key, model_name, messages):
    client = openai.OpenAI(
        base_url="https://cryptotalks.ai/v1",
        api_key=api_key
    )
    completion = client.chat.completions.create(
        model=model_name,  
        messages=messages,
    )
    return completion.choices[0].message.content

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    session_id = data.get('sessionId')  # Expect a sessionId from the client
    if not session_id:
        return jsonify({'error': 'Session ID is required'}), 400
    
    api_key = data.get('apiKey')
    model_name = data.get('modelName', 'model-default')
    user_message = data.get('message', '')
    
    if not api_key or not user_message:
        return jsonify({'error': 'API key and message are required'}), 400

    # Retrieve conversation history
    messages = get_conversation_history(session_id)
    messages.append({"role": "user", "content": user_message})

    response = chat_with_openai(api_key, model_name, messages)
    # Store new messages
    add_message_to_db(session_id, "user", user_message)
    add_message_to_db(session_id, "assistant", response)

    return jsonify({'response': response})

@app.route('/models', methods=['GET'])
def get_models():
    response = requests.get('https://cryptotalks.ai/v1/models/')
    if response.status_code == 200:
        models = response.json().get('data', [])
        return jsonify(models)
    else:
        return jsonify({'error': 'Failed to fetch models'}), 500

if __name__ == "__main__":
    app.run(debug=True)
    setup_database()
