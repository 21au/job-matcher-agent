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

PARSER_PROMPT = """Kamu adalah CV Parser Specialist. Ubah teks mentah CV menjadi 
data terstruktur dalam format JSON.

Ekstrak:
- name: nama lengkap
- email: alamat email
- skills: daftar skill teknis (list of string)
- experience: daftar pengalaman kerja/organisasi (list of string, singkat)
- education: daftar pendidikan (list of string)

PENTING: Balas HANYA dengan JSON valid, tanpa teks tambahan, tanpa markdown backticks.

Teks CV:
{cv_text}
"""

def parse_cv(cv_text: str) -> dict:
    prompt = PARSER_PROMPT.format(cv_text=cv_text)
    response = llm.invoke(prompt)
    raw_output = response.content.strip()
    raw_output = raw_output.replace("```json", "").replace("```", "").strip()
    
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        print("Gagal parse JSON. Output mentah:")
        print(raw_output)
        return {}


if __name__ == "__main__":
    from tools.pdf_extractor import extract_text_from_pdf
    from tools.supabase_client import save_cv
    
    cv_path = "data/cvs/cv_saya.pdf"
    cv_text = extract_text_from_pdf(cv_path)
    cv_data = parse_cv(cv_text)
    
    print("=== HASIL PARSING ===")
    print(json.dumps(cv_data, indent=2, ensure_ascii=False))
    
    saved = save_cv(cv_data, cv_text)
    if saved:
        print(f"\nCV tersimpan ke Supabase dengan ID: {saved['id']}")