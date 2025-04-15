# app/utils/resume_processing.py

import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to extract text from resume using PyMuPDF
def extract_text_from_resume(filepath):
    try:
        text = ""
        doc = fitz.open(filepath)
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print("Error extracting text:", e)
        return ""

# Dummy job dataset — Replace with your own real dataset or database integration
job_dataset = [
    {
        'title': 'Data Analyst',
        'company': 'Google',
        'description': 'Analyze big data, build dashboards, Python, SQL, Excel'
    },
    {
        'title': 'Software Engineer',
        'company': 'Microsoft',
        'description': 'Develop software, Python, Java, problem-solving, algorithms'
    },
    {
        'title': 'AI Researcher',
        'company': 'OpenAI',
        'description': 'NLP, deep learning, transformer models, PyTorch'
    }
]

# Function to match resume text to job descriptions using TF-IDF + cosine similarity
def match_resume_to_jobs(resume_text):
    results = []

    try:
        job_descriptions = [job['description'] for job in job_dataset]
        all_texts = [resume_text] + job_descriptions

        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(all_texts)

        cosine_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

        for idx, score in enumerate(cosine_scores):
            job = job_dataset[idx]
            job_result = {
                'title': job['title'],
                'company': job['company'],
                'score': round(score * 100, 2),
                'description': job['description']
            }
            results.append(job_result)

        results = sorted(results, key=lambda x: x['score'], reverse=True)

    except Exception as e:
        print("Error matching resume:", e)

    return results
