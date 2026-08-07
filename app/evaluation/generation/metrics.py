def answer_relevance(answer: str, expected_keywords: list[str]) -> float:
    if not expected_keywords:
        return 1.0 if "couldn't find" in answer.lower() else 0.0

    answer = answer.lower()
    matched = sum(1 for keyword in expected_keywords if keyword.lower() in answer)

    return round(matched / len(expected_keywords), 3)


def citation_accuracy(predicted_sources: list[str], expected_sources: list[str]) -> float:
    if not expected_sources:
        return 1.0 if not predicted_sources else 0.0

    matches = set(predicted_sources).intersection(set(expected_sources))

    return round(len(matches) / len(expected_sources), 3)


def faithfulness(answer: str, context: str) -> float:

    refusal_phrases = [
        "couldn't find",
        "could not find",
        "not enough evidence",
        "no information",
    ]

    answer_lower = answer.lower()

    if any(phrase in answer_lower for phrase in refusal_phrases):
        return 1.0

    answer_words = set(answer_lower.split())
    context_words = set(context.lower().split())

    if not answer_words:
        return 0.0

    supported_words = answer_words.intersection(context_words)

    return round(len(supported_words) / len(answer_words),3)