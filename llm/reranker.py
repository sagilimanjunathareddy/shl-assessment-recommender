from sentence_transformers import CrossEncoder


cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query, candidates, top_k=10):
    """
    Re-rank FAISS retrieved candidates using CrossEncoder.
    
    Args:
        query (str): User query
        candidates (list): List of assessment dicts
        top_k (int): Number of results to return
    
    Returns:
        list: Top-k reranked candidates
    """

    if not candidates:
        return []

    
    pairs = [
        (query, c["name"] + " " + c.get("description", ""))
        for c in candidates
    ]

    
    scores = cross_encoder.predict(pairs)

   
    scored_candidates = list(zip(candidates, scores))

 
    scored_candidates.sort(key=lambda x: x[1], reverse=True)

    
    return [c[0] for c in scored_candidates[:top_k]]