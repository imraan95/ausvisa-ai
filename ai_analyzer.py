import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# You can get a free API token from Hugging Face: https://huggingface.co/settings/tokens
API_TOKEN = os.getenv('HUGGING_FACE_TOKEN', '')
API_URL = "https://api-inference.huggingface.co/models/facebook/opt-1.3b"  # Free model

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def load_training_data():
    """Load visa profiles from CSV for context"""
    if not os.path.exists('data/visa_profiles.csv'):
        return "No historical visa data available."
    
    with open('data/visa_profiles.csv', 'r') as f:
        return f.read()

def create_system_prompt():
    """Create system prompt with training data"""
    training_data = load_training_data()
    
    return f"""You are an AI visa assessment assistant for Australian immigration.
Your role is to analyze visa applications and provide detailed recommendations.
Use this historical visa data for context:

{training_data}

Analyze each profile considering:
1. Points calculation based on age, education, experience, and English level
2. Visa type recommendations (189, 190, 491, etc.)
3. Occupation list matches
4. State/Territory nomination possibilities
5. Processing time estimates
6. Success probability"""

def query_model(payload):
    """Query the Hugging Face model"""
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        print(f"Error querying model: {str(e)}")
        return None

def analyze_profile(profile):
    """Analyze a visa profile using Hugging Face model"""
    try:
        # Create a detailed prompt for the profile
        system_prompt = create_system_prompt()
        profile_prompt = f"""Please analyze this visa profile:
- Age: {profile.get('age')} years
- Education: {profile.get('education_level')}
- Work Experience: {profile.get('work_experience')} years
- English Proficiency: {profile.get('english_proficiency')}

Provide a detailed assessment including points calculation, visa recommendations, 
and specific next steps."""

        full_prompt = f"{system_prompt}\n\n{profile_prompt}"
        
        # Query the model
        response = query_model({
            "inputs": full_prompt,
            "parameters": {
                "max_length": 1000,
                "temperature": 0.7,
                "num_return_sequences": 1
            }
        })
        
        if response and isinstance(response, list) and len(response) > 0:
            return response[0].get('generated_text', '').strip()
        
        return None
        
    except Exception as e:
        print(f"Error in AI analysis: {str(e)}")
        return None

def get_visa_requirements():
    """Get detailed visa requirements using the model"""
    try:
        prompt = """Please provide detailed requirements for the following Australian visas:
1. Skilled Independent Visa (Subclass 189)
2. Skilled Nominated Visa (Subclass 190)
3. Skilled Work Regional (Provisional) Visa (Subclass 491)

Include points requirements, eligibility criteria, and application process."""

        response = query_model({
            "inputs": prompt,
            "parameters": {
                "max_length": 1000,
                "temperature": 0.7,
                "num_return_sequences": 1
            }
        })
        
        if response and isinstance(response, list) and len(response) > 0:
            return response[0].get('generated_text', '').strip()
        
        return None
        
    except Exception as e:
        print(f"Error getting visa requirements: {str(e)}")
        return None
