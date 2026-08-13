def can_generate_answer(confidence: dict) -> bool:
    score = confidence.get("confidence_score", 0.0)

    return score >= 0.45