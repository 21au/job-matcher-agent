import feedparser

# Daftar sumber RSS feed
RSS_SOURCES = {
    "remoteok": "https://remoteok.com/remote-dev-jobs.rss",
    "weworkremotely": "https://weworkremotely.com/categories/remote-programming-jobs.rss",
}


def fetch_jobs_from_rss(source_name: str) -> list[dict]:
    """
    Ambil daftar lowongan dari 1 sumber RSS feed.
    
    Args:
        source_name: key dari RSS_SOURCES (misal 'remoteok')
    
    Returns:
        list of dict, masing-masing berisi title, company, description, url
    """
    if source_name not in RSS_SOURCES:
        raise ValueError(f"Sumber '{source_name}' tidak dikenal. Pilihan: {list(RSS_SOURCES.keys())}")
    
    feed_url = RSS_SOURCES[source_name]
    feed = feedparser.parse(feed_url)
    
    jobs = []
    for entry in feed.entries:
        job = {
            "source": source_name,
            "title": entry.get("title", "No title"),
            "company": entry.get("author", "Unknown"),
            "description": entry.get("summary", ""),
            "url": entry.get("link", ""),
        }
        jobs.append(job)
    
    return jobs


def fetch_all_jobs() -> list[dict]:
    """
    Ambil lowongan dari SEMUA sumber RSS yang terdaftar.
    
    Returns:
        list gabungan semua lowongan dari semua sumber
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
    
    new_jobs = save_multiple_jobs(jobs)
    print(f"Lowongan BARU yang disimpan ke Supabase: {len(new_jobs)}")
    
    if new_jobs:
        print("\n=== Contoh lowongan baru yang disimpan ===")
        for job in new_jobs[:3]:
            print(f"\nJudul: {job['title']}")
            print(f"Company: {job['company']}")
            print(f"URL: {job['url']}")