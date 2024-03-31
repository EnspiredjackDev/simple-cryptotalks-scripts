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
    total_tokens_used = completion.usage.total_tokens
    total_cost = completion.usage.model_extra['total_cost']
    message_content = completion.choices[0].message.content

    return {
        'message_content': message_content,
        'total_tokens_used': total_tokens_used,
        'total_cost': total_cost
    }

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

    chat_response = chat_with_openai(api_key, model_name, messages)
    message_content = chat_response['message_content']
    
    # Store new messages
    add_message_to_db(session_id, "user", user_message)
    add_message_to_db(session_id, "assistant", message_content)

    # Return the message content along with total tokens used and total cost
    return jsonify({
        'response': message_content,
        'total_tokens_used': chat_response['total_tokens_used'],
        'total_cost': chat_response['total_cost']
    })

@app.route('/models', methods=['GET'])
def get_models():
    response = requests.get('https://cryptotalks.ai/v1/models/')
    if response.status_code == 200:
        models_data = response.json().get('data', [])
        
        # Transform the models_data to include both model names and their IDs
        model_details = [{'name': model.get('name'), 'id': model.get('id')} for model in models_data]
        
        return jsonify(model_details)
    else:
        return jsonify({'error': 'Failed to fetch models'}), 500


@app.route('/model-details', methods=['GET'])
def get_model_details():
    model_id = request.args.get('modelId', '')
    response = requests.get('https://cryptotalks.ai/v1/models/')
    if response.status_code == 200:
        models_data = response.json().get('data', [])
        
        # Find the specific model by ID
        model_detail = next((model for model in models_data if model.get('id') == model_id), None)
        
        if model_detail is not None:
            pricing_info = model_detail.get('pricing', {})
            adjusted_pricing = {}
            for key, value in pricing_info.items():
                if key in ['prompt', 'completion'] and isinstance(value, (float, int)):
                    # Adjust the pricing to per 1000 tokens for prompt and completion
                    adjusted_pricing[key] = round(value * 1000, 4)
                elif key == 'image':
                    # Leave the image pricing as is
                    adjusted_pricing[key] = value
            
            model_detail['pricing'] = adjusted_pricing  # Replace pricing with adjusted pricing
            
            return jsonify(model_detail)
        else:
            return jsonify({'error': 'Model not found'}), 404
    else:
        return jsonify({'error': 'Failed to fetch models'}), 500

if __name__ == "__main__":
    setup_database()
    app.run(debug=True)
    