import pandas as pd
from retrieval.retriever import retrieve
from evaluation.recall_at_k import recall_at_k


def extract_slug(url):
    return url.rstrip("/").split("/")[-1]


train_df = pd.read_csv("data/train/labeled_train.csv")

queries = train_df["Query"].unique()
recalls = []

for query in queries:
    true_urls = train_df[train_df["Query"] == query]["Assessment_url"].tolist()
    true_slugs = [extract_slug(u) for u in true_urls]

    predictions = retrieve(query, top_k=10)
    predicted_slugs = [extract_slug(p["url"]) for p in predictions]

    score = recall_at_k(true_slugs, predicted_slugs, k=10)
    recalls.append(score)

mean_recall = sum(recalls) / len(recalls)

print(f"Mean Recall@10: {mean_recall:.4f}")