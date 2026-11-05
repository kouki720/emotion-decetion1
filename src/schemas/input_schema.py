
from pydantic import BaseModel, Field, field_validator


class SentimentInput(BaseModel):
    text: str = Field(
        ...,
        min_length=2,
        max_length=5000,
        description="Texte à analyser"
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Le texte ne doit pas être vide.")

        return value
