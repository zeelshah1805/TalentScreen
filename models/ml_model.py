from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
import numpy as np
import pickle
import os

class MLResumeModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.feature_columns = [
            'skill_count', 'experience_years', 'education_score', 
            'job_match_score', 'word_count', 'sentence_count'
        ]
        self.is_trained = False
    
    def prepare_features(self, resume_data):
        """Prepare features for machine learning"""
        features = []
        for data in resume_data:
            feature_vector = [
                len(data['skills']),
                data['experience_years'],
                data['education_score'],
                data['job_match_score'],
                len(data['text'].split()),
                len(data['text'].split('.'))
            ]
            features.append(feature_vector)
        return np.array(features)
    
    def train_model(self, training_data, labels):
        """Train the machine learning model"""
        X = self.prepare_features(training_data)
        y = np.array(labels)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        print(f"Model Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(report)
        
        self.is_trained = True
        return accuracy, report
    
    def predict(self, resume_data):
        """Predict resume quality"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        features = self.prepare_features([resume_data])
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0]
        
        return {
            'prediction': prediction,
            'confidence': max(probability),
            'probabilities': {
                'poor': probability[0],
                'fair': probability[1],
                'good': probability[2],
                'excellent': probability[3]
            }
        }
    
    def save_model(self, filepath):
        """Save trained model to file"""
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
    
    def load_model(self, filepath):
        """Load trained model from file"""
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                self.model = pickle.load(f)
                self.is_trained = True
                return True
        return False

# Sample training data generator
def generate_sample_data():
    """Generate sample training data for demonstration"""
    np.random.seed(42)
    
    data = []
    labels = []
    
    for _ in range(1000):
        # Generate synthetic resume data
        skill_count = np.random.randint(1, 20)
        experience = np.random.randint(0, 15)
        education = np.random.uniform(0, 1)
        job_match = np.random.uniform(0, 1)
        
        # Create synthetic text
        text = " ".join(["word"] * np.random.randint(100, 1000))
        
        resume_data = {
            'skills': ['skill'] * skill_count,
            'experience_years': experience,
            'education_score': education,
            'job_match_score': job_match,
            'text': text
        }
        
        # Generate label based on features
        score = (skill_count/20 + experience/15 + education + job_match) / 4
        if score >= 0.8:
            label = 3  # Excellent
        elif score >= 0.6:
            label = 2  # Good
        elif score >= 0.4:
            label = 1  # Fair
        else:
            label = 0  # Poor
        
        data.append(resume_data)
        labels.append(label)
    
    return data, labels

import os

if __name__ == "__main__":
    # Train and save model
    model = MLResumeModel()
    training_data, labels = generate_sample_data()
    
    accuracy, report = model.train_model(training_data, labels)
    
    save_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, 'trained_model.pkl')
    
    model.save_model(save_path)
    
    print("Model trained and saved successfully!")
