
from collections import Counter
from typing import Any

from langchain_core.tools import tool


@tool
def calculate_sentiment_statistics(results: list[dict[str, Any]]) -> dict:
    """
    Calcule les statistiques d'une collection de résultats
    d'analyse de sentiment.
    """

    if not isinstance(results, list) or not results:
        raise ValueError(
            "La liste des résultats ne doit pas être vide."
        )

    total = len(results)

    sentiments = []
    emotions = []
    languages = []
    confidences = []

    for index, result in enumerate(results):

        if not isinstance(result, dict):
            raise ValueError(
                f"Le résultat {index} doit être un dictionnaire."
            )

        sentiment = result.get("sentiment")
        emotion = result.get("emotion")
        language = result.get("language")
        confidence = result.get("confidence")

        if not isinstance(sentiment, str) or not sentiment.strip():
            raise ValueError(
                f"Sentiment invalide dans le résultat {index}."
            )

        if not isinstance(emotion, str) or not emotion.strip():
            raise ValueError(
                f"Émotion invalide dans le résultat {index}."
            )

        if not isinstance(language, str) or not language.strip():
            raise ValueError(
                f"Langue invalide dans le résultat {index}."
            )

        if (
            isinstance(confidence, bool)
            or not isinstance(confidence, (int, float))
            or not 0.0 <= confidence <= 1.0
        ):
            raise ValueError(
                f"Confidence invalide dans le résultat {index}."
            )

        sentiments.append(sentiment)
        emotions.append(emotion)
        languages.append(language)
        confidences.append(float(confidence))

    sentiment_counts = Counter(sentiments)
    emotion_counts = Counter(emotions)
    language_counts = Counter(languages)

    sentiment_percentages = {
        key: round((count / total) * 100, 2)
        for key, count in sentiment_counts.items()
    }

    emotion_percentages = {
        key: round((count / total) * 100, 2)
        for key, count in emotion_counts.items()
    }

    language_percentages = {
        key: round((count / total) * 100, 2)
        for key, count in language_counts.items()
    }

    return {
        "total_analyzed": total,
        "sentiment_distribution": dict(sentiment_counts),
        "sentiment_percentages": sentiment_percentages,
        "dominant_sentiment": sentiment_counts.most_common(1)[0][0],
        "emotion_distribution": dict(emotion_counts),
        "emotion_percentages": emotion_percentages,
        "language_distribution": dict(language_counts),
        "language_percentages": language_percentages,
        "average_confidence": round(
            sum(confidences) / total, 4
        )
    }
