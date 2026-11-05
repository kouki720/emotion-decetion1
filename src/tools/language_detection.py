
from langdetect import DetectorFactory, detect_langs, LangDetectException
from langchain_core.tools import tool


# Garantit des résultats reproductibles
DetectorFactory.seed = 0


LANGUAGE_NAMES = {
    "fr": "French",
    "en": "English",
    "ar": "Arabic",
    "es": "Spanish",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "zh-cn": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "tr": "Turkish",
    "nl": "Dutch",
    "hi": "Hindi",
}


@tool
def detect_language(text: str) -> dict:
    """
    Detecte automatiquement la langue d'un texte.

    Retourne le code de langue, son nom et
    le niveau de confiance de la détection.
    """

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Le texte ne doit pas être vide.")

    text = text.strip()

    if len(text) < 3:
        raise ValueError(
            "Le texte est trop court pour détecter sa langue."
        )

    try:
        predictions = detect_langs(text)

        best_prediction = predictions[0]

        language_code = best_prediction.lang
        language_name = LANGUAGE_NAMES.get(
            language_code,
            language_code
        )

        confidence = round(best_prediction.prob, 4)

        return {
            "language_code": language_code,
            "language": language_name,
            "confidence": confidence
        }

    except LangDetectException as error:
        raise ValueError(
            "Impossible de détecter la langue du texte."
        ) from error
