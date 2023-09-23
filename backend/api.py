from flask import Flask, request, jsonify
import uuid
import requests
from flask_cors import CORS
import datetime
from models import get_model
from chatbots import get_chatbot


# Initialize the Flask application
app = Flask(__name__)
CORS(app)
@app.route('/initiate', methods=['GET'])
def initiate():
    # Generate a unique UUID for the new conversation
    conversation_id = str(uuid.uuid4())
    # Return the conversation ID to the client
    return jsonify({'conversation_id': conversation_id})


# Define a route for the default URL, which loads the chatbot
@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Get user message from POST request
    try:
        message = request.json['message']
        conversation_id = request.json['conversation_id']
        model_name = request.json['model']
        chatbot_type = request.json['type']
        context = request.json["context"]

    except KeyError:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        model = get_model(model_name)
        chat = get_chatbot(model, chatbot_type)
        response = chat(message, context, conversation_id)

    except Exception as e:
        print(e)

    return jsonify({'message':response.message})

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



