import json
from tools.pdf_extractor import extract_text_from_pdf
from tools.rss_fetcher import fetch_all_jobs
from tools.supabase_client import (
    save_multiple_jobs, get_latest_cv, save_cv,
    get_unprocessed_jobs, save_match_result, get_all_cvs
)
from agents.parser_agent import parse_cv
from agents.matcher_agent import match_cv_to_multiple_jobs
from agents.notifier_agent import notify_high_matches

MAX_JOBS_PER_RUN = 15  # batasi biar nggak kena rate limit Groq


def ensure_cv_exists():
    """
    Pastikan minimal ada 1 CV tersimpan. Kalau belum ada sama sekali,
    parse dari file lokal sebagai CV pertama.
    """
    cvs = get_all_cvs()
    if cvs:
        return cvs

    print("Belum ada CV tersimpan, parsing dari file lokal...")
    cv_text = extract_text_from_pdf("data/cvs/cv_saya.pdf")
    cv_data = parse_cv(cv_text)
    saved = save_cv(cv_data, cv_text)
    print(f"CV baru tersimpan dengan ID: {saved['id']}")
    return [saved]


def process_cv(cv: dict):
    """
    Jalankan matching untuk 1 CV terhadap semua lowongan yang belum diproses.
    """
    print(f"\n--- Memproses CV: {cv.get('name')} (ID: {cv['id']}) ---")

    unprocessed = get_unprocessed_jobs(cv["id"])
    if len(unprocessed) > MAX_JOBS_PER_RUN:
        print(f"Ada {len(unprocessed)} lowongan baru, diproses {MAX_JOBS_PER_RUN} dulu (sisanya di run berikutnya)")
        unprocessed = unprocessed[:MAX_JOBS_PER_RUN]
    else:
        print(f"Lowongan yang perlu dianalisis: {len(unprocessed)}")

    if not unprocessed:
        print("Tidak ada lowongan baru untuk CV ini.")
        return

    cv_data = {
        "skills": cv.get("skills", []),
        "experience": cv.get("experience", []),
        "education": cv.get("education", [])
    }
    results = match_cv_to_multiple_jobs(cv_data, unprocessed)

    for result in results:
        save_match_result(cv["id"], result["job"]["id"], result["match"])

    notified = notify_high_matches(results)
    print(f"Notifikasi terkirim untuk CV ini: {notified}")


def run_pipeline():
    print("=== JOB MATCHER AGENT (Multi-CV) ===\n")

    cvs = ensure_cv_exists()
    print(f"Total CV aktif yang akan diproses: {len(cvs)}")

    print("\n[1] Fetching lowongan dari RSS...")
    jobs = fetch_all_jobs()
    new_jobs = save_multiple_jobs(jobs)
    print(f"Lowongan baru tersimpan: {len(new_jobs)}")

    print("\n[2] Memproses setiap CV...")
    for cv in cvs:
        try:
            process_cv(cv)
        except Exception as e:
            print(f"GAGAL memproses CV '{cv.get('name')}': {e}")
            print("Lanjut ke CV berikutnya...")
            continue


if __name__ == "__main__":
    run_pipeline()