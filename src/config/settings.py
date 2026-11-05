import os
from pathlib import Path

from dotenv import load_dotenv


# Racine du projet
BASE_DIR = Path(__file__).resolve().parents[2]

# Chargement des variables d'environnement
load_dotenv(BASE_DIR / ".env")

# Clé API Google Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")


def validate_settings():
    """Vérifie la configuration nécessaire au projet."""

    if not GOOGLE_API_KEY:
        raise ValueError(
            "GOOGLE_API_KEY est absente. "
            "Vérifiez votre fichier .env."
        )

    if len(GOOGLE_API_KEY.strip()) < 20:
        raise ValueError("La clé API Google semble invalide.")


if __name__ == "__main__":
    validate_settings()

    print("Configuration chargée avec succès.")
    print("Google Gemini API Key : configurée (valeur masquée)")