import os
import pickle
import random

def create_sample_data():
    """Create a sample dataset if none exists"""
    data = []
    for _ in range(100):
        profile = {
            'age': random.randint(20, 60),
            'education_level': random.choice(['Bachelor', 'Master', 'PhD']),
            'work_experience': random.randint(0, 20),
            'english_proficiency': random.choice(['Basic', 'Intermediate', 'Advanced']),
            'visa_granted': random.choice([0, 1], p=[0.3, 0.7])
        }
        data.append(profile)
    return data

def calculate_score(profile):
    """Calculate visa success probability based on profile attributes"""
    score = 0
    max_score = 100
    
    # Age scoring (25-32 gets maximum points)
    age = profile.get('age', 30)
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
        'Diploma': 5
    }
    score += education_scores.get(profile.get('education_level', 'Bachelor'), 0)
    
    # Work experience scoring
    experience = profile.get('work_experience', 0)
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
        'Advanced': 20,
        'Intermediate': 15,
        'Basic': 5
    }
    score += english_scores.get(profile.get('english_proficiency', 'Intermediate'), 0)
    
    return score / max_score

def get_visa_recommendations(probability):
    """Get visa recommendations based on probability score"""
    if probability >= 0.7:
        return {
            'recommendation': 'Skilled Independent Visa (Subclass 189)',
            'confidence': 'High',
            'processing_time': '12-16 months',
            'cost': 'AUD 4,115'
        }
    elif probability >= 0.5:
        return {
            'recommendation': 'Skilled Nominated Visa (Subclass 190)',
            'confidence': 'Medium',
            'processing_time': '9-12 months',
            'cost': 'AUD 4,115'
        }
    else:
        return {
            'recommendation': 'Consider improving your profile or exploring other visa options',
            'confidence': 'Low',
            'suggestion': 'Focus on improving English proficiency or gaining more work experience'
        }

if __name__ == '__main__':
    # Create sample data if it doesn't exist
    if not os.path.exists('data/visa_profiles.csv'):
        data = create_sample_data()
        os.makedirs('data', exist_ok=True)
        with open('data/visa_profiles.csv', 'w') as f:
            for profile in data:
                f.write(','.join(map(str, profile.values())) + '\n')
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Save the scoring functions
    with open('models/visa_model.pkl', 'wb') as f:
        pickle.dump({
            'calculate_score': calculate_score,
            'get_recommendations': get_visa_recommendations
        }, f)
