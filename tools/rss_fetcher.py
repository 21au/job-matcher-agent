import feedparser

RSS_SOURCES = {
    "remoteok": "https://remoteok.com/remote-dev-jobs.rss",
    "weworkremotely": "https://weworkremotely.com/categories/remote-programming-jobs.rss",
}


def extract_company_and_title(entry: dict) -> tuple[str, str]:
    """
    Coba ekstrak nama company dan judul lowongan yang bersih.
    Banyak RSS feed job board nyimpen company di dalam title,
    formatnya "Nama Company: Judul Lowongan".
    
    Returns:
        tuple (company, title)
    """
    raw_title = entry.get("title", "No title")
    author = entry.get("author", "").strip()
    
    # Prioritas 1: field 'author' kalau ada isinya
    if author:
        return author, raw_title
    
    # Prioritas 2: parsing dari title, format "Company: Job Title"
    if ":" in raw_title:
        parts = raw_title.split(":", 1)
        possible_company = parts[0].strip()
        possible_title = parts[1].strip()
        # Validasi sederhana: nama company biasanya nggak terlalu panjang
        if 0 < len(possible_company) <= 60:
            return possible_company, possible_title
    
    # Fallback: nggak ketemu company yang jelas
    return "Tidak diketahui", raw_title


def fetch_jobs_from_rss(source_name: str) -> list[dict]:
    """
    Ambil daftar lowongan dari 1 sumber RSS feed.
    """
    if source_name not in RSS_SOURCES:
        raise ValueError(f"Sumber '{source_name}' tidak dikenal. Pilihan: {list(RSS_SOURCES.keys())}")
    
    feed_url = RSS_SOURCES[source_name]
    feed = feedparser.parse(feed_url)
    
    jobs = []
    for entry in feed.entries:
        company, title = extract_company_and_title(entry)
        job = {
            "source": source_name,
            "title": title,
            "company": company,
            "description": entry.get("summary", ""),
            "url": entry.get("link", ""),
        }
        jobs.append(job)
    
    return jobs


def fetch_all_jobs() -> list[dict]:
    """
    Ambil lowongan dari SEMUA sumber RSS yang terdaftar.
    """
    all_jobs = []
    for source_name in RSS_SOURCES:
        try:
            jobs = fetch_jobs_from_rss(source_name)
            all_jobs.extend(jobs)
            print(f"[{source_name}] Berhasil ambil {len(jobs)} lowongan")
        except Exception as e:
            print(f"[{source_name}] Gagal fetch: {e}")
    
    return all_jobs


if __name__ == "__main__":
    from tools.supabase_client import save_multiple_jobs
    
    jobs = fetch_all_jobs()
    print(f"\nTotal lowongan ditemukan dari RSS: {len(jobs)}")
    
    if jobs:
        print("\n=== Contoh hasil parsing company ===")
        for job in jobs[:5]:
            print(f"Company: {job['company']:30} | Title: {job['title'][:50]}")
    
    new_jobs = save_multiple_jobs(jobs)
    print(f"\nLowongan BARU yang disimpan ke Supabase: {len(new_jobs)}")