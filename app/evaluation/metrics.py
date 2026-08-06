def recall_at_k(retrieved_ids: list[str], relevant_ids: list[str], k: int):
    retrieved_top_k = retrieved_ids[:k]
    relevant_found = set(retrieved_top_k).intersection(set(relevant_ids))
    return 1.0 if relevant_found else 0.0


def precision_at_k(retrieved_ids: list[str], relevant_ids: list[str], k: int):
    retrieved_top_k = retrieved_ids[:k]
    relevant_found = set(retrieved_top_k).intersection(set(relevant_ids))
    return len(relevant_found) / k


def reciprocal_rank(retrieved_ids: list[str], relevant_ids: list[str]):
    for rank, chunk_id in enumerate(retrieved_ids, start=1):
        if chunk_id in relevant_ids:
            return 1 / rank
    return 0.0