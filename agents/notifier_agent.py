import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.telegram_sender import send_telegram_message

MIN_SCORE_TO_NOTIFY = 60  # threshold skor minimal biar dinotif


def format_match_notification(job: dict, match: dict) -> str:
    """
    Format hasil matching jadi pesan Telegram yang rapi.
    """
    score = match.get("score", 0)
    matched = ", ".join(match.get("matched_skills", []))
    missing = ", ".join(match.get("missing_skills", []))
    summary = match.get("summary", "")
    
    message = f"""🎯 *Lowongan Baru Cocok!*

*{job.get('title')}*
🏢 {job.get('company')}
📊 Skor: *{score}/100*

✅ Match: {matched}
⚠️ Gap: {missing}

📝 {summary}

🔗 {job.get('url')}
"""
    return message


def notify_high_matches(results: list[dict]) -> int:
    """
    Kirim notifikasi Telegram untuk lowongan dengan skor di atas threshold.
    
    Args:
        results: list of dict {job, match} dari match_cv_to_multiple_jobs
    
    Returns:
        jumlah notifikasi yang berhasil dikirim
    """
    notified_count = 0
    for result in results:
        score = result["match"].get("score", 0)
        if score >= MIN_SCORE_TO_NOTIFY:
            message = format_match_notification(result["job"], result["match"])
            success = send_telegram_message(message)
            if success:
                notified_count += 1
    
    return notified_count