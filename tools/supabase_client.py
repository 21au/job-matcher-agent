import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_job_posting(job: dict) -> dict | None:
    """
    Simpan 1 lowongan ke tabel job_postings.
    Kalau URL sudah ada (duplikat), skip dan return None.
    
    Args:
        job: dict berisi source, title, company, description, url
    
    Returns:
        dict data yang tersimpan, atau None kalau duplikat/gagal
    """
    # Cek duplikat berdasarkan URL
    existing = supabase.table("job_postings").select("id").eq("url", job["url"]).execute()
    
    if existing.data:
        return None  # Sudah ada, skip
    
    result = supabase.table("job_postings").insert({
        "source": job["source"],
        "title": job["title"],
        "company": job["company"],
        "description": job["description"],
        "url": job["url"],
    }).execute()
    
    return result.data[0] if result.data else None


def save_multiple_jobs(jobs: list[dict]) -> list[dict]:
    """
    Simpan banyak lowongan sekaligus, skip yang duplikat.
    
    Args:
        jobs: list of dict lowongan
    
    Returns:
        list of dict lowongan yang BARU berhasil disimpan (bukan duplikat)
    """
    new_jobs = []
    for job in jobs:
        saved = save_job_posting(job)
        if saved:
            new_jobs.append(saved)
    
    return new_jobs


def get_unprocessed_jobs(cv_id: int) -> list[dict]:
    """
    Ambil lowongan yang BELUM pernah di-match dengan CV tertentu.
    
    Args:
        cv_id: ID CV yang mau dicek
    
    Returns:
        list of job_postings yang belum ada di tabel matches untuk cv_id ini
    """
    all_jobs = supabase.table("job_postings").select("*").execute().data
    
    matched_job_ids = supabase.table("matches").select("job_id").eq("cv_id", cv_id).execute().data
    matched_ids_set = {m["job_id"] for m in matched_job_ids}
    
    unprocessed = [job for job in all_jobs if job["id"] not in matched_ids_set]
    return unprocessed


def save_cv(cv_data: dict, raw_text: str) -> dict | None:
    """
    Simpan CV yang sudah di-parse ke tabel cvs.
    
    Args:
        cv_data: dict hasil parsing (name, email, skills, experience, education)
        raw_text: teks mentah CV
    
    Returns:
        dict data CV yang tersimpan, termasuk id-nya
    """
    result = supabase.table("cvs").insert({
        "name": cv_data.get("name"),
        "email": cv_data.get("email"),
        "skills": cv_data.get("skills", []),
        "experience": cv_data.get("experience", []),
        "education": cv_data.get("education", []),
        "raw_text": raw_text,
    }).execute()
    
    return result.data[0] if result.data else None


def get_latest_cv() -> dict | None:
    """
    Ambil CV terakhir yang disimpan (sementara asumsi 1 CV aktif).
    
    Returns:
        dict data CV, atau None kalau belum ada CV tersimpan
    """
    result = supabase.table("cvs").select("*").order("created_at", desc=True).limit(1).execute()
    return result.data[0] if result.data else None


def save_match_result(cv_id: int, job_id: int, matcher_result: dict) -> dict | None:
    """
    Simpan hasil matching CV vs lowongan.
    
    Args:
        cv_id: ID CV
        job_id: ID lowongan
        matcher_result: dict berisi score, matched_skills, missing_skills, summary
    
    Returns:
        dict data match yang tersimpan
    """
    result = supabase.table("matches").insert({
        "cv_id": cv_id,
        "job_id": job_id,
        "score": matcher_result.get("score", 0),
        "matched_skills": matcher_result.get("matched_skills", []),
        "missing_skills": matcher_result.get("missing_skills", []),
        "summary": matcher_result.get("summary", ""),
        "notified": False,
    }).execute()
    
    return result.data[0] if result.data else None