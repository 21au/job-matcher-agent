import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

MATCHER_PROMPT = """Kamu adalah CV-Job Matcher Specialist. Bandingkan skill kandidat 
dengan deskripsi lowongan berikut, lalu berikan skor kecocokan.

DATA CV KANDIDAT:
Skills: {skills}
Experience: {experience}
Education: {education}

LOWONGAN:
Judul: {job_title}
Deskripsi: {job_description}

Berikan output JSON:
{{
  "score": <angka 0-100>,
  "matched_skills": [<skill yang match>],
  "missing_skills": [<requirement penting yang belum dimiliki>],
  "summary": "<ringkasan 2-3 kalimat>"
}}

PENTING: Balas HANYA dengan JSON valid, tanpa teks tambahan, tanpa markdown backticks.
"""

def match_cv_to_job(cv_data: dict, job: dict) -> dict:
    """
    Bandingkan 1 CV dengan 1 lowongan.
    
    Args:
        cv_data: dict CV (skills, experience, education)
        job: dict lowongan (title, description)
    
    Returns:
        dict hasil matching
    """
    prompt = MATCHER_PROMPT.format(
        skills=", ".join(cv_data.get("skills", [])),
        experience=", ".join(cv_data.get("experience", [])),
        education=", ".join(cv_data.get("education", [])),
        job_title=job.get("title", ""),
        job_description=job.get("description", "")[:1500]  # batasi panjang biar hemat token
    )
    
    response = llm.invoke(prompt)
    raw_output = response.content.strip()
    raw_output = raw_output.replace("```json", "").replace("```", "").strip()
    
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        print(f"Gagal parse JSON untuk job '{job.get('title')}'. Output mentah:")
        print(raw_output)
        return {}


def match_cv_to_multiple_jobs(cv_data: dict, jobs: list[dict]) -> list[dict]:
    """
    Bandingkan 1 CV dengan banyak lowongan sekaligus.
    
    Args:
        cv_data: dict CV
        jobs: list of dict lowongan
    
    Returns:
        list of dict, masing-masing berisi job info + hasil matching
    """
    results = []
    for job in jobs:
        print(f"Matching: {job.get('title')}...")
        match_result = match_cv_to_job(cv_data, job)
        if match_result:
            results.append({
                "job": job,
                "match": match_result
            })
    return results