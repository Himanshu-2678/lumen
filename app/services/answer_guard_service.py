def can_generate_answer(confidence: dict) -> bool:
    if confidence["confidence_level"] == "low":
        return False

    return True