from flask import Flask, render_template, jsonify, request, send_from_directory
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

app = Flask(__name__)

# Configure for production
app.config['ENV'] = os.environ.get('FLASK_ENV', 'production')
app.config['DEBUG'] = False if app.config['ENV'] == 'production' else True

# Serve static files
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# Load and preprocess the data
def load_data():
    try:
        data = pd.read_csv('data/visa_profiles.csv')
        required_columns = ['age', 'education_level', 'work_experience', 'english_proficiency', 
                          'occupation', 'salary_range', 'visa_granted']
        
        # Initialize missing columns with default values
        for col in required_columns:
            if col not in data.columns:
                if col == 'visa_granted':
                    data[col] = data.get('visa_outcome', 0)
                else:
                    data[col] = 'Unknown'
        
        return data
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        # Return a minimal dataset if file is not found or is invalid
        return pd.DataFrame(columns=['age', 'education_level', 'work_experience', 'english_proficiency', 
                                   'occupation', 'salary_range', 'visa_granted'])

# Train the model
def train_model(data):
    # Prepare features and target
    X = data.drop(['visa_granted', 'timeline_months', 'cost_aud'], axis=1)
    
    # Convert categorical variables
    X = pd.get_dummies(X, columns=['education_level', 'english_proficiency', 'occupation', 'salary_range'])
    y = data['visa_granted']
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)
    
    return model, scaler, X.columns.tolist()  # Save feature names for prediction

# Calculate visa success probability based on profile attributes
def calculate_score(profile):
    """Calculate visa success probability based on profile attributes"""
    score = 0
    max_score = 100
    
    # Age scoring (25-32 gets maximum points)
    age = int(profile['age'])
    if 25 <= age <= 32:
        score += 30
    elif 33 <= age <= 39:
        score += 25
    elif 18 <= age <= 24:
        score += 20
    elif 40 <= age <= 44:
        score += 15
    
    # Education scoring
    education_scores = {
        'PhD': 20,
        'Master': 15,
        'Bachelor': 10,
        'Diploma': 5,
        'Certificate': 3
    }
    score += education_scores.get(profile['education_level'], 0)
    
    # Work experience scoring
    experience = int(profile['work_experience'])
    if experience >= 8:
        score += 20
    elif experience >= 5:
        score += 15
    elif experience >= 3:
        score += 10
    elif experience >= 1:
        score += 5
    
    # English proficiency scoring
    english_scores = {
        'Superior': 20,
        'Proficient': 15,
        'Competent': 10,
        'Basic': 5
    }
    score += english_scores.get(profile['english_proficiency'], 0)
    
    # Salary range scoring
    salary_scores = {
        '200000+': 10,
        '150000-200000': 8,
        '100000-150000': 6,
        '70000-100000': 4,
        '50000-70000': 2,
        '40000-50000': 1,
        '0-40000': 0
    }
    score += salary_scores.get(profile['salary_range'], 0)
    
    return score / max_score

# Generate visa recommendations based on profile and probability
def get_visa_recommendations(profile_data, probability):
    """Generate visa recommendations based on profile and probability"""
    recommendations = []
    
    if probability >= 0.7:
        if int(profile_data['work_experience']) >= 5:
            recommendations.append({
                'visa_type': 'Skilled Independent Visa (Subclass 189)',
                'confidence': 'High',
                'details': 'Based on your strong profile, you have excellent chances for this permanent residency pathway.'
            })
        recommendations.append({
            'visa_type': 'Skilled Nominated Visa (Subclass 190)',
            'confidence': 'High',
            'details': 'Your profile matches well with state nomination requirements.'
        })
    
    elif probability >= 0.4:
        recommendations.append({
            'visa_type': 'Temporary Skill Shortage Visa (Subclass 482)',
            'confidence': 'Medium',
            'details': 'Consider this temporary work visa to build your experience in Australia.'
        })
        if profile_data['education_level'] in ['Bachelor', 'Master', 'PhD']:
            recommendations.append({
                'visa_type': 'Graduate Temporary Visa (Subclass 485)',
                'confidence': 'Medium',
                'details': 'This could be a good pathway if you\'ve recently completed studies in Australia.'
            })
    
    else:
        recommendations.append({
            'visa_type': 'Student Visa (Subclass 500)',
            'confidence': 'Medium',
            'details': 'Consider upgrading your qualifications through Australian education.'
        })
        recommendations.append({
            'visa_type': 'Training Visa (Subclass 407)',
            'confidence': 'Low',
            'details': 'This could help you gain relevant Australian experience.'
        })
    
    return recommendations

# Routes
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
        # Load the trained model and feature names
        model = joblib.load('models/visa_model.joblib')
        scaler = joblib.load('models/scaler.joblib')
        feature_names = joblib.load('models/feature_names.joblib')
        
        # TODO: Implement proper NLP processing
        # For now, return a simple response
        response = {
            'response': 'Based on the information provided, I estimate a 75% success probability for your visa application. The typical processing time is 6-8 months, and the cost ranges from AUD 3,000 to AUD 4,000. Would you like more specific details about any particular aspect?'
        }
    except Exception as e:
        print(f"Error in chat processing: {str(e)}")
        response = {
            'response': 'I apologize, but I encountered an error while processing your request. Please try again or rephrase your question.'
        }
    
    return jsonify(response)

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Calculate probability
        success_probability = calculate_score(data)
        
        # Generate visa recommendations
        visa_recommendations = get_visa_recommendations(data, success_probability)
        
        return jsonify({
            'success_probability': success_probability,
            'recommendations': visa_recommendations
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    # Load data and train model
    data = load_data()
    
    try:
        model, scaler, feature_names = train_model(data)
        
        # Save model and scaler
        if not os.path.exists('models'):
            os.makedirs('models')
        joblib.dump(model, 'models/visa_model.joblib')
        joblib.dump(scaler, 'models/scaler.joblib')
        joblib.dump(feature_names, 'models/feature_names.joblib')
    except Exception as e:
        print(f"Error training model: {str(e)}")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
