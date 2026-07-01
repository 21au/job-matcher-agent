\# 🎯 Job Matcher Agent



Sistem multi-agent AI yang secara otomatis memindai lowongan kerja baru, mencocokkannya dengan profil kandidat menggunakan LLM, dan mengirim notifikasi real-time untuk kecocokan tinggi — dilengkapi dashboard interaktif.



🔗 \*\*Live Demo:\*\* https://job-matcher-agent-omega.vercel.app



\## Arsitektur



\## Fitur



\- \*\*Multi-agent pipeline\*\*: Parser, Matcher, dan Notifier Agent yang saling terhubung

\- \*\*RAG-based matching\*\*: skor kecocokan CV vs lowongan menggunakan LLM (Groq/Llama 3.3)

\- \*\*Otomasi terjadwal\*\*: GitHub Actions menjalankan pipeline setiap 6 jam

\- \*\*Notifikasi real-time\*\*: Telegram bot untuk kecocokan skor tinggi

\- \*\*Dashboard interaktif\*\*: visualisasi hasil matching dengan desain custom (React + Tailwind + Framer Motion)



\## Tech Stack



\*\*Backend:\*\* Python, LangChain, Groq API, Supabase, feedparser

\*\*Frontend:\*\* React (Vite), Tailwind CSS v4, Framer Motion

\*\*Infrastruktur:\*\* GitHub Actions (scheduler), Vercel (hosting), Supabase (database)



\## Cara Kerja



1\. \*\*Fetcher Agent\*\* mengambil lowongan terbaru dari RSS feed job board

2\. \*\*Parser Agent\*\* mengekstrak data CV (skill, pengalaman, pendidikan) dari PDF menjadi JSON terstruktur

3\. \*\*Matcher Agent\*\* membandingkan CV dengan setiap lowongan baru menggunakan LLM, menghasilkan skor kecocokan 0-100 beserta analisis gap skill

4\. \*\*Notifier Agent\*\* mengirim notifikasi Telegram untuk lowongan dengan skor ≥60

5\. Seluruh hasil tersimpan di Supabase dan ditampilkan di dashboard



\## Setup Lokal



```bash

git clone https://github.com/21au/job-matcher-agent.git

cd job-matcher-agent

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt

```



Isi `.env` dengan API key yang diperlukan (lihat `.env.example`), lalu jalankan:



```bash

python main.py

```



\## Roadmap



\- \[ ] Support multi-CV per user

\- \[ ] Tambah sumber RSS feed job board Indonesia

\- \[ ] Filter kategori role/seniority



\---



Dibuat oleh \*\*Audrey Pramudita Sudarmanto\*\* — \[LinkedIn](#) · \[Portfolio](#)

