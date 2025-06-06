# Resume Screening Web Application

## Project Description
This project is a Flask-based web application designed to screen resumes against job descriptions using machine learning and natural language processing techniques. It allows users to upload resumes and job descriptions, processes them to evaluate the quality and relevance of resumes, and provides analytics and detailed results through a user-friendly web interface.

## Features
- Upload single or multiple resumes for screening.
- Compare resumes against job descriptions to assess match quality.
- Machine learning model classifies resumes into categories: Poor, Fair, Good, Excellent.
- Extracts text from PDF, DOCX, and TXT resume files.
- Provides analytics dashboard with visualizations using Plotly.
- REST API endpoints for bulk processing and analytics data.
- Easy-to-use web interface with upload and results pages.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application
Run the Flask application using:
```bash
python app.py
```
The app will start in debug mode and be accessible at `http://127.0.0.1:5000/`.

### Web Interface
- Navigate to the home page (`/`) to access the main dashboard.
- Use the upload page (`/upload`) to upload resumes and enter a job description.
- After processing, results will be displayed with resume quality scores and details.

### API Endpoints
- `POST /api/bulk_process`: Upload multiple resumes and a job description for bulk screening. Returns JSON results.
- `GET /api/analytics`: Retrieves analytics data for dashboard visualizations.

## Machine Learning Model

The project uses a RandomForestClassifier model to classify resumes into four categories: Poor, Fair, Good, and Excellent. The model uses features such as skill count, years of experience, education score, job match score, word count, and sentence count extracted from resumes.

### Training the Model
The model can be trained using synthetic data generated within the `models/ml_model.py` script. To train and save the model, run:
```bash
python models/ml_model.py
```
This will train the model and save it as `trained_model.pkl` in the `models/` directory.

## Project Structure

```
.
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── data/                   # Sample job descriptions and resumes
├── models/                 # Machine learning models and processors
│   ├── ml_model.py         # ML model definition and training
│   ├── resume_processor.py # Resume processing logic
│   └── trained_model.pkl   # Pre-trained model file
├── static/                 # Static files (CSS, JS)
├── templates/              # HTML templates for Flask
├── utils/                  # Utility modules (text extraction, preprocessing)
├── uploads/                # Temporary upload storage
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation (this file)
```

## Adding Screenshots of Output

To add screenshots of the application output to this README:

1. Create a folder in the project directory to store screenshots, e.g., `docs/screenshots/`.
2. Save your screenshots in this folder.
3. Add images to this README using Markdown syntax:


![Landing Page](docs\screenshots\landing1.png)


![Landing Page Continue](docs\screenshots\landing2.png)

![Resume Screening](docs\screenshots\screening.png)

![Output](docs\screenshots\output.png)


## Dependencies

- Flask==2.3.3
- spacy==3.7.2
- scikit-learn==1.3.0
- pandas==2.0.3
- numpy==1.23.5
- nltk==3.8.1
- PyPDF2==3.0.1
- python-docx==0.8.11
- plotly==5.15.0
- Werkzeug==2.3.7

## License

This project is licensed under the MIT License. See the LICENSE file for details.
