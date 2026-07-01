from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


def get_embedding(text: str) -> list[float]:
    """
    Generate embedding vector dari teks.
    
    Args:
        text: teks yang mau di-embed
    
    Returns:
        list of float, embedding vector
    """
    return embedding_model.encode(text).tolist()


def compute_similarity(text1: str, text2: str) -> float:
    """
    Hitung cosine similarity antara 2 teks (opsional, buat quick filter
    sebelum kirim ke LLM biar hemat API call).
    """
    from sentence_transformers.util import cos_sim
    emb1 = embedding_model.encode(text1, convert_to_tensor=True)
    emb2 = embedding_model.encode(text2, convert_to_tensor=True)
    return float(cos_sim(emb1, emb2)[0][0])