from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename
from models.resume_processor import ResumeProcessor
from utils.text_extractor import extract_text_from_file
import plotly.graph_objs as go
import plotly.utils

app = Flask(__name__)
app.config.from_object('config.Config')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize resume processor
processor = ResumeProcessor()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/upload')
def upload_page():
    """Resume upload page"""
    return render_template('upload.html')

@app.route('/process_resume', methods=['POST'])
def process_resume():
    """Process uploaded resume and job description"""
    try:
        if 'resume' not in request.files:
            flash('No resume file uploaded')
            return redirect(request.url)
        
        file = request.files['resume']
        job_description = request.form.get('job_description', '')
        
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract text from file
            resume_text = extract_text_from_file(filepath)
            
            # Process resume
            results = processor.screen_resume(resume_text, job_description)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return render_template('results.html', 
                                 results=results, 
                                 filename=filename,
                                 resume_text=resume_text[:500] + "..." if len(resume_text) > 500 else resume_text)
        
        flash('Invalid file type. Please upload PDF, DOCX, or TXT files.')
        return redirect(request.url)
        
    except Exception as e:
        flash(f'Error processing resume: {str(e)}')
        return redirect(url_for('upload_page'))

@app.route('/api/bulk_process', methods=['POST'])
def bulk_process():
    """API endpoint for bulk resume processing"""
    try:
        files = request.files.getlist('resumes')
        job_description = request.form.get('job_description', '')
        
        results = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                resume_text = extract_text_from_file(filepath)
                result = processor.screen_resume(resume_text, job_description)
                result['filename'] = filename
                results.append(result)
                
                os.remove(filepath)
        
        return jsonify({'results': results})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics')
def analytics():
    """Get analytics data for dashboard"""
    # Mock analytics data - in real app, this would come from database
    data = {
        'total_resumes': 156,
        'excellent_matches': 23,
        'good_matches': 45,
        'fair_matches': 67,
        'poor_matches': 21,
        'recent_activity': [
            {'name': 'John Doe', 'score': 0.85, 'status': 'Excellent'},
            {'name': 'Jane Smith', 'score': 0.72, 'status': 'Good'},
            {'name': 'Bob Johnson', 'score': 0.58, 'status': 'Fair'},
        ]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)