from flask import Flask, request, jsonify
import uuid
from flask_cors import CORS
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

@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Get data from POST request
    try:
        data = request.get_json()
        message = data['message']
        conversation_id = data['conversation_id']
        model_name = data['model']
        chatbot_type = data['type']
        images = data.get('images', [])
        file_path = data.get('file_path', '')

    except KeyError as e:
        return jsonify({'error': f'Missing key: {e.args[0]}'}), 400

    try:
        # Create or retrieve the chatbot instance based on conversation_id
        chatbot = get_chatbot(model_name, chatbot_type)
        
        # If images or file_path are provided, use them, otherwise pass an empty list/string
        if images or file_path:
            if chatbot_type == "simple_chatbot":
                response_content = chatbot.chat(message, images=images)
            elif chatbot_type == "write_code_from_file":
                response_content = chatbot.chat(message, filepath=file_path)
        else:
            # This assumes that your chatbot has a default chat method taking only a message.
            response_content = chatbot.chat(message)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'response': response_content})

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
