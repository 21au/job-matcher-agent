import json
from tools.pdf_extractor import extract_text_from_pdf
from tools.rss_fetcher import fetch_all_jobs
from tools.supabase_client import (
    save_multiple_jobs, get_latest_cv, save_cv, 
    get_unprocessed_jobs, save_match_result
)
from agents.parser_agent import parse_cv
from agents.matcher_agent import match_cv_to_multiple_jobs
from agents.notifier_agent import notify_high_matches


def ensure_cv_exists():
    """
    Pastikan ada CV tersimpan di Supabase. Kalau belum ada, parse dari file lokal.
    """
    cv = get_latest_cv()
    if cv:
        print(f"Menggunakan CV tersimpan: {cv['name']} (ID: {cv['id']})")
        return cv
    
    print("Belum ada CV tersimpan, parsing dari file lokal...")
    cv_text = extract_text_from_pdf("data/cvs/cv_saya.pdf")
    cv_data = parse_cv(cv_text)
    saved = save_cv(cv_data, cv_text)
    print(f"CV baru tersimpan dengan ID: {saved['id']}")
    return saved


def run_pipeline():
    """
    Orchestrator utama: fetch lowongan -> match ke CV -> notif kalau cocok.
    """
    print("=== JOB MATCHER AGENT ===\n")
    
    # 1. Pastikan CV ada
    cv = ensure_cv_exists()
    
    # 2. Fetch lowongan terbaru dari RSS
    print("\n[1] Fetching lowongan dari RSS...")
    jobs = fetch_all_jobs()
    new_jobs = save_multiple_jobs(jobs)
    print(f"Lowongan baru tersimpan: {len(new_jobs)}")
    
    # 3. Ambil semua lowongan yang belum pernah di-match dengan CV ini
    print("\n[2] Mengecek lowongan yang belum diproses...")
    unprocessed = get_unprocessed_jobs(cv["id"])
    MAX_JOBS_PER_RUN = 15  # batasi biar nggak kena rate limit Groq
    if len(unprocessed) > MAX_JOBS_PER_RUN:
        print(f"Ada {len(unprocessed)} lowongan baru, diproses {MAX_JOBS_PER_RUN} dulu (sisanya di run berikutnya)")
        unprocessed = unprocessed[:MAX_JOBS_PER_RUN]
    else:
        print(f"Lowongan yang perlu dianalisis: {len(unprocessed)}")
    
    if not unprocessed:
        print("Tidak ada lowongan baru untuk dianalisis. Selesai.")
        return
    
    # 4. Matching CV ke semua lowongan baru
    print("\n[3] Menjalankan matching...")
    cv_data = {
        "skills": cv.get("skills", []),
        "experience": cv.get("experience", []),
        "education": cv.get("education", [])
    }
    results = match_cv_to_multiple_jobs(cv_data, unprocessed)
    
    # 5. Simpan hasil matching ke Supabase
    print("\n[4] Menyimpan hasil matching...")
    for result in results:
        save_match_result(cv["id"], result["job"]["id"], result["match"])
    
    # 6. Kirim notifikasi Telegram untuk yang skornya tinggi
    print("\n[5] Mengirim notifikasi Telegram...")
    notified = notify_high_matches(results)
    print(f"Notifikasi terkirim: {notified}")
    
    print("\n=== SELESAI ===")


if __name__ == "__main__":
    run_pipeline()