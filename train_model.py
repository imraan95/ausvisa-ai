import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

def train_model():
    # Create a simple dummy dataset if the CSV doesn't exist
    if not os.path.exists('data/visa_profiles.csv'):
        data = pd.DataFrame({
            'age': np.random.randint(20, 60, 100),
            'education_level': np.random.choice(['Bachelor', 'Master', 'PhD'], 100),
            'work_experience': np.random.randint(0, 20, 100),
            'english_proficiency': np.random.choice(['Basic', 'Intermediate', 'Advanced'], 100),
            'visa_granted': np.random.choice([0, 1], 100, p=[0.3, 0.7])
        })
        os.makedirs('data', exist_ok=True)
        data.to_csv('data/visa_profiles.csv', index=False)
    else:
        data = pd.read_csv('data/visa_profiles.csv')

    # Prepare features
    X = pd.get_dummies(data.drop('visa_granted', axis=1))
    y = data['visa_granted']

    # Train a simple model
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)

    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)

    # Save the model and feature names
    with open('models/visa_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('models/feature_names.pkl', 'wb') as f:
        pickle.dump(X.columns.tolist(), f)

if __name__ == '__main__':
    train_model()
