import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestClassifier
import pickle
import os
import re
from utils.preprocessing import preprocess_text

class ResumeProcessor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
        self.model = None
        self.load_model()
        
        # Skills database
        self.skills_db = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust'],
            'web_development': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'django', 'flask'],
            'data_science': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'matplotlib'],
            'databases': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'],
            'soft_skills': ['leadership', 'communication', 'teamwork', 'problem-solving', 'analytical']
        }
    
    def load_model(self):
        """Load pre-trained model if exists"""
        model_path = 'models/trained_model.pkl'
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
    
    def extract_skills(self, text):
        """Extract skills from resume text"""
        text_lower = text.lower()
        extracted_skills = []
        
        for category, skills in self.skills_db.items():
            for skill in skills:
                if skill.lower() in text_lower:
                    extracted_skills.append(skill)
        
        return list(set(extracted_skills))
    
    def extract_experience(self, text):
        """Extract years of experience from resume"""
        doc = self.nlp(text)
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+?\s*yrs?\s*(?:of\s*)?experience',
            r'experience\s*:?\s*(\d+)\+?\s*years?',
        ]
        
        years = []
        for pattern in experience_patterns:
            matches = re.findall(pattern, text.lower())
            years.extend([int(match) for match in matches])
        
        return max(years) if years else 0
    
    def extract_education(self, text):
        """Extract education information"""
        education_keywords = [
            'bachelor', 'master', 'phd', 'doctorate', 'degree', 'university', 'college',
            'b.s.', 'b.a.', 'm.s.', 'm.a.', 'mba', 'ph.d.'
        ]
        
        text_lower = text.lower()
        education_score = sum(1 for keyword in education_keywords if keyword in text_lower)
        return min(education_score / len(education_keywords), 1.0)
    
    def calculate_similarity(self, resume_text, job_description):
        """Calculate similarity between resume and job description"""
        if not job_description:
            return 0.5  # Default score if no job description
        
        documents = [preprocess_text(resume_text), preprocess_text(job_description)]
        tfidf_matrix = self.tfidf.fit_transform(documents)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return similarity[0][0]
    
    def screen_resume(self, resume_text, job_description=""):
        """Main function to screen a resume"""
        # Extract features
        skills = self.extract_skills(resume_text)
        experience = self.extract_experience(resume_text)
        education_score = self.extract_education(resume_text)
        similarity_score = self.calculate_similarity(resume_text, job_description)
        
        # Calculate overall score
        skill_score = min(len(skills) / 10, 1.0)  # Normalize to 0-1
        experience_score = min(experience / 10, 1.0)  # 10+ years = 1.0
        
        # Weighted average
        overall_score = (
            skill_score * 0.4 +
            experience_score * 0.3 +
            education_score * 0.2 +
            similarity_score * 0.1
        )
        
        # Determine status
        if overall_score >= 0.8:
            status = "Excellent"
        elif overall_score >= 0.6:
            status = "Good"
        elif overall_score >= 0.4:
            status = "Fair"
        else:
            status = "Poor"
        
        return {
            'overall_score': round(overall_score, 2),
            'status': status,
            'skills': skills,
            'experience_years': experience,
            'education_score': round(education_score, 2),
            'job_match_score': round(similarity_score, 2),
            'breakdown': {
                'skills': round(skill_score, 2),
                'experience': round(experience_score, 2),
                'education': round(education_score, 2),
                'job_match': round(similarity_score, 2)
            }
        }