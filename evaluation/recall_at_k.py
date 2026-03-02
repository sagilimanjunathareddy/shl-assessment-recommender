def recall_at_k(true_urls, predicted_urls, k=10):
    predicted = predicted_urls[:k]
    relevant = set(true_urls)

    retrieved_relevant = len([url for url in predicted if url in relevant])
    return retrieved_relevant / len(relevant) if relevant else 0