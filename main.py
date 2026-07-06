import json
from tools.logger import setup_logger
from tools.pdf_extractor import extract_text_from_pdf
from tools.rss_fetcher import fetch_all_jobs
from tools.supabase_client import (
    save_multiple_jobs, get_latest_cv, save_cv,
    get_unprocessed_jobs, save_match_result, get_all_cvs
)
from agents.parser_agent import parse_cv
from agents.matcher_agent import match_cv_to_multiple_jobs
from agents.notifier_agent import notify_high_matches

logger = setup_logger("main")

MAX_JOBS_PER_RUN = 15


def ensure_cv_exists():
    cvs = get_all_cvs()
    if cvs:
        return cvs

    logger.info("Belum ada CV tersimpan, parsing dari file lokal...")
    cv_text = extract_text_from_pdf("data/cvs/cv_saya.pdf")
    cv_data = parse_cv(cv_text)
    saved = save_cv(cv_data, cv_text)
    logger.info(f"CV baru tersimpan dengan ID: {saved['id']}")
    return [saved]


def process_cv(cv: dict):
    logger.info(f"--- Memproses CV: {cv.get('name')} (ID: {cv['id']}) ---")

    unprocessed = get_unprocessed_jobs(cv["id"])
    if len(unprocessed) > MAX_JOBS_PER_RUN:
        logger.info(f"Ada {len(unprocessed)} lowongan baru, diproses {MAX_JOBS_PER_RUN} dulu (sisanya di run berikutnya)")
        unprocessed = unprocessed[:MAX_JOBS_PER_RUN]
    else:
        logger.info(f"Lowongan yang perlu dianalisis: {len(unprocessed)}")

    if not unprocessed:
        logger.info("Tidak ada lowongan baru untuk CV ini.")
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
    logger.info(f"Notifikasi terkirim untuk CV ini: {notified}")


def run_pipeline():
    logger.info("=== JOB MATCHER AGENT (Multi-CV) START ===")

    cvs = ensure_cv_exists()
    logger.info(f"Total CV aktif yang akan diproses: {len(cvs)}")

    logger.info("[1] Fetching lowongan dari RSS...")
    jobs = fetch_all_jobs()
    new_jobs = save_multiple_jobs(jobs)
    logger.info(f"Lowongan baru tersimpan: {len(new_jobs)}")

    logger.info("[2] Memproses setiap CV...")
    for cv in cvs:
        try:
            process_cv(cv)
        except Exception as e:
            logger.error(f"GAGAL memproses CV '{cv.get('name')}': {e}")
            logger.info("Lanjut ke CV berikutnya...")
            continue

    logger.info("=== SELESAI ===")


if __name__ == "__main__":
    run_pipeline()