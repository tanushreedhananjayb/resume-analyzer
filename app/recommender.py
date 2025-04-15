# app/recommender.py

import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch
import os

# Load job dataset
# app/recommender.py

CSV_PATH = os.path.join(os.getcwd(), 'jobs.csv')
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError("The jobs.csv file was not found. Make sure it exists in the root directory.")

jobs_df = pd.read_csv(CSV_PATH)


# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Embed all job descriptions
job_descriptions = jobs_df['job_description'].fillna('').astype(str).tolist()
job_embeddings = model.encode(job_descriptions, convert_to_tensor=True)

def match_resume_to_jobs(resume_text, top_n=5):
    """
    Compare resume text with job descriptions and return top N matches.
    """
    # Embed resume
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)

    # Compute cosine similarity
    similarities = util.cos_sim(resume_embedding, job_embeddings)[0]

    # Get top N similar jobs
    top_indices = torch.topk(similarities, k=top_n).indices

    matches = []
    for idx in top_indices:
        idx = idx.item()
        job = jobs_df.iloc[idx]
        score = float(similarities[idx]) * 100  # convert to percentage

        matches.append({
            'title': job.get('job_title', 'N/A'),
            'company': job.get('company', 'N/A'),
            'description': job.get('job_description', '')[:1000],  # limit long text
            'score': round(score, 2)
        })

    return matches
