
from pydantic import ValidationError

from src.schemas.sentiment_schema import SentimentResult


def validate_sentiment_output(data: dict) -> SentimentResult:
    """
    Valide et retourne un résultat d'analyse de sentiment
    conforme au schéma SentimentResult.
    """

    if not isinstance(data, dict):
        raise TypeError(
            "Le résultat doit être un dictionnaire."
        )

    try:
        result = SentimentResult.model_validate(data)

    except ValidationError as error:
        raise ValueError(
            f"Résultat de sentiment invalide :\n{error}"
        ) from error

    return result


def validate_sentiment_result(
    result: SentimentResult
) -> bool:
    """
    Vérifie qu'un objet SentimentResult est valide.
    """

    if not isinstance(result, SentimentResult):
        raise TypeError(
            "L'objet fourni doit être une instance de SentimentResult."
        )

    validate_sentiment_output(result.model_dump())

    return True
