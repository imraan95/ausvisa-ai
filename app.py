from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__)

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/chat')
def chat():
    return send_from_directory('.', 'chat.html')

@app.route('/api/chat', methods=['POST'])
def process_chat():
    message = request.json.get('message', '')
    response = {
        'response': 'Based on your message, I estimate a 75% success probability for your visa application. Would you like more specific details about any particular aspect?'
    }
    return jsonify(response)

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
