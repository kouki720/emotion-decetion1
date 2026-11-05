
from typing import Literal
from pydantic import BaseModel, Field


class SentimentResult(BaseModel):

    sentiment: Literal[
        "very_positive",
        "positive",
        "slightly_positive",
        "neutral",
        "slightly_negative",
        "negative",
        "very_negative"
    ] = Field(
        description="Catégorie et polarité du sentiment détecté"
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Niveau de confiance de la classification entre 0 et 1"
    )

    intensity: Literal[
        "very_low",
        "low",
        "moderate",
        "high",
        "very_high"
    ] = Field(
        description="Intensité du sentiment exprimé"
    )

    emotion: Literal[
        "joy",
        "sadness",
        "anger",
        "fear",
        "surprise",
        "disgust",
        "trust",
        "anticipation",
        "frustration",
        "disappointment",
        "satisfaction",
        "neutral"
    ] = Field(
        description="Émotion dominante détectée"
    )

    language: str = Field(
        description="Langue détectée"
    )

    explanation: str = Field(
    default="Explication non fournie par le modèle.",
    description=(
        "Explication courte et objective justifiant "
        "la classification du sentiment et de l'émotion"
    )
)
