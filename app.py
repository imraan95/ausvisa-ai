from flask import Flask, jsonify, request, send_from_directory
import os
import pickle
import re

app = Flask(__name__)

# Load the model
try:
    with open('models/visa_model.pkl', 'rb') as f:
        model = pickle.load(f)
    calculate_score = model['calculate_score']
    get_recommendations = model['get_recommendations']
except Exception as e:
    print(f"Error loading model: {str(e)}")
    calculate_score = None
    get_recommendations = None

def extract_profile_from_message(message):
    """Extract profile information from user message"""
    profile = {}
    
    # Extract age
    age_match = re.search(r'(\d+)\s*(?:years?\s*old|years?\s*of\s*age)', message.lower())
    if age_match:
        profile['age'] = int(age_match.group(1))
    
    # Extract education
    education_levels = ['PhD', 'Master', 'Bachelor', 'Diploma']
    for edu in education_levels:
        if edu.lower() in message.lower():
            profile['education_level'] = edu
            break
    
    # Extract work experience
    exp_match = re.search(r'(\d+)\s*years?\s*(?:of\s*)?(?:work\s*)?experience', message.lower())
    if exp_match:
        profile['work_experience'] = int(exp_match.group(1))
    
    # Extract English proficiency
    if 'advanced' in message.lower() or 'fluent' in message.lower():
        profile['english_proficiency'] = 'Advanced'
    elif 'intermediate' in message.lower() or 'good' in message.lower():
        profile['english_proficiency'] = 'Intermediate'
    elif 'basic' in message.lower() or 'beginner' in message.lower():
        profile['english_proficiency'] = 'Basic'
    
    return profile

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
        # Extract profile information from message
        profile = extract_profile_from_message(message)
        
        if not profile:
            return jsonify({
                'response': 'Could you please provide more information about your age, education, work experience, and English proficiency?'
            })
        
        # Calculate probability
        probability = calculate_score(profile)
        
        # Get recommendations
        recommendations = get_recommendations(probability)
        
        # Format response
        response = f"Based on your profile, I estimate a {int(probability * 100)}% success probability for your visa application.\n\n"
        response += f"Recommended Visa: {recommendations['recommendation']}\n"
        response += f"Confidence: {recommendations['confidence']}\n"
        
        if 'processing_time' in recommendations:
            response += f"Processing Time: {recommendations['processing_time']}\n"
        if 'cost' in recommendations:
            response += f"Estimated Cost: {recommendations['cost']}\n"
        if 'suggestion' in recommendations:
            response += f"\nSuggestion: {recommendations['suggestion']}"
        
        return jsonify({'response': response})
    
    except Exception as e:
        print(f"Error in chat processing: {str(e)}")
        return jsonify({
            'response': 'I apologize, but I encountered an error while processing your request. Please try again with more specific information about your profile.'
        })

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
