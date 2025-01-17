from flask import Flask, render_template, jsonify, request, send_from_directory
import pickle
import os

app = Flask(__name__)

# Load the pre-trained model and feature names
try:
    with open('models/visa_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('models/feature_names.pkl', 'rb') as f:
        feature_names = pickle.load(f)
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None
    feature_names = None

# Serve static files
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
    
    try:
        # For now, return a simple response
        response = {
            'response': 'Based on the information provided, I estimate a 75% success probability for your visa application. Would you like more specific details about any particular aspect?'
        }
    except Exception as e:
        print(f"Error in chat processing: {str(e)}")
        response = {
            'response': 'I apologize, but I encountered an error while processing your request. Please try again.'
        }
    
    return jsonify(response)

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
