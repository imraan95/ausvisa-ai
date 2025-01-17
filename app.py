from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World!'

@app.route('/api/chat', methods=['POST'])
def process_chat():
    message = request.json.get('message', '')
    response = {
        'response': 'Thank you for your message. Our AI assistant is currently being updated. Please try again later.'
    }
    return jsonify(response)

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
