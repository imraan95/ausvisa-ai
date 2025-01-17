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
        if edu.lower() in message.lower() or f"{edu}'s".lower() in message.lower():
            profile['education_level'] = edu
            break
    
    # Extract work experience
    exp_match = re.search(r'(\d+)\s*years?\s*(?:of\s*)?(?:work\s*)?experience', message.lower())
    if exp_match:
        profile['work_experience'] = int(exp_match.group(1))
    
    # Extract English proficiency
    if any(word in message.lower() for word in ['fluent', 'advanced', 'excellent', 'native']):
        profile['english_proficiency'] = 'Advanced'
    elif any(word in message.lower() for word in ['intermediate', 'good', 'moderate']):
        profile['english_proficiency'] = 'Intermediate'
    elif any(word in message.lower() for word in ['basic', 'beginner', 'elementary']):
        profile['english_proficiency'] = 'Basic'
    
    return profile

def generate_missing_fields_message(profile):
    """Generate a message asking for missing information"""
    missing = []
    if 'age' not in profile:
        missing.append("age")
    if 'education_level' not in profile:
        missing.append("education level (e.g., Bachelor's, Master's, PhD)")
    if 'work_experience' not in profile:
        missing.append("years of work experience")
    if 'english_proficiency' not in profile:
        missing.append("English proficiency level (Basic, Intermediate, or Advanced)")
    
    if not missing:
        return None
    
    return f"Could you please provide your {', '.join(missing[:-1])}{',' if len(missing) > 2 '' if len(missing) == 1 else ' and'} {missing[-1]}?"

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
        
        # Check for missing information
        missing_fields_msg = generate_missing_fields_message(profile)
        if missing_fields_msg:
            return jsonify({'response': missing_fields_msg})
        
        # Calculate probability
        probability = calculate_score(profile)
        
        # Get recommendations
        recommendations = get_recommendations(probability)
        
        # Format response
        response = f"Based on your profile:\n"
        response += f"- Age: {profile.get('age')} years\n"
        response += f"- Education: {profile.get('education_level')}\n"
        response += f"- Work Experience: {profile.get('work_experience')} years\n"
        response += f"- English Proficiency: {profile.get('english_proficiency')}\n\n"
        
        response += f"I estimate a {int(probability * 100)}% success probability for your visa application.\n\n"
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
