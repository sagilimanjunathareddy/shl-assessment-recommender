import json
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("data/processed/shl_catalog_cleaned.json", "r", encoding="utf-8") as f:
    data = json.load(f)

texts = []
metadata = []

for item in data:
    text = f"""
    Assessment Name: {item.get('name', '')}

    Description: {item.get('description', '')}

    Test Type: {', '.join(item.get('test_type', []))}

    Duration: {item.get('duration', '')} minutes

    Remote Support: {item.get('remote_support', '')}

    Adaptive Support: {item.get('adaptive_support', '')}
    """

    texts.append(text)
    metadata.append(item)

embeddings = model.encode(texts, show_progress_bar=True)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

faiss.write_index(index, "data/embeddings/faiss_index.bin")

with open("data/embeddings/metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

print("Embeddings regenerated successfully.")