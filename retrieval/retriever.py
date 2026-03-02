import faiss
import numpy as np
import pickle
import re
from sentence_transformers import SentenceTransformer
from llm.reranker import rerank

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("data/embeddings/faiss_index.bin")

with open("data/embeddings/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)



TECH_KEYWORDS = [
    "java", "python", "sql", "javascript", "c++", "c#", "cloud",
    "data", "analytics", "developer", "programming"
]

SOFT_KEYWORDS = [
    "collaborate", "team", "communication", "leadership",
    "stakeholder", "interpersonal", "behavior", "personality"
]


def extract_keywords(query):
    query_lower = query.lower()
    tech = [k for k in TECH_KEYWORDS if k in query_lower]
    soft = [k for k in SOFT_KEYWORDS if k in query_lower]
    return tech, soft


def boost_candidates(candidates, tech_keywords, soft_keywords):
    boosted = []

    for c in candidates:
        text = (c["name"] + " " + c.get("description", "")).lower()
        score = 0

        # boost technical matches
        for k in tech_keywords:
            if k in text:
                score += 2

        # boost soft skill matches
        for k in soft_keywords:
            if k in text:
                score += 1.5

        boosted.append((c, score))

    boosted.sort(key=lambda x: x[1], reverse=True)

    return [c[0] for c in boosted]


def retrieve(query, top_k=10):

   
    query_embedding = embedding_model.encode([query])
    distances, indices = index.search(np.array(query_embedding), 75)

    candidates = [metadata[i] for i in indices[0]]

   
    tech_keywords, soft_keywords = extract_keywords(query)

   
    boosted_candidates = boost_candidates(
        candidates, tech_keywords, soft_keywords
    )

    
    reranked = rerank(query, boosted_candidates[:40], top_k=top_k)

    return reranked