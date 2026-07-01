import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(text: str) -> bool:
    """
    Kirim pesan teks ke Telegram.
    
    Args:
        text: isi pesan (support Markdown formatting)
    
    Returns:
        True kalau berhasil, False kalau gagal
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    response = requests.post(url, data=payload)
    return response.status_code == 200


if __name__ == "__main__":
    success = send_telegram_message("🎉 Test notifikasi dari Job Matcher Agent berhasil!")
    print("Berhasil terkirim!" if success else "Gagal kirim pesan.")