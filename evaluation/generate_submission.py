import pandas as pd
from retrieval.retriever import retrieve

test_df = pd.read_csv("data/test/unlabeled_test.csv")

results = []

for query in test_df["Query"]:
    predictions = retrieve(query, top_k=10)
    urls = [p["url"] for p in predictions]

    results.append({
        "Query": query,
        "Recommended_Assessments": ",".join(urls)
    })

submission_df = pd.DataFrame(results)
submission_df.to_csv("submission.csv", index=False)

print("Submission file created.")