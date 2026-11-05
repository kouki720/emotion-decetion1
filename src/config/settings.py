import os
from pathlib import Path

from dotenv import load_dotenv


# Racine du projet
BASE_DIR = Path(__file__).resolve().parents[2]

# Charger les variables du fichier .env
load_dotenv(BASE_DIR / ".env")

# Configuration Hugging Face
HF_TOKEN = os.getenv("HF_TOKEN")

# Modèle utilisé pour l'analyse de sentiment
HF_MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"


def validate_settings():

    if not HF_TOKEN:
        raise ValueError(
            "HF_TOKEN est absent. Vérifiez votre fichier .env."
        )

    if not HF_TOKEN.startswith("hf_"):
        raise ValueError(
            "Le token Hugging Face semble invalide."
        )


if __name__ == "__main__":
    validate_settings()

    print("Configuration chargée avec succès.")
    print(f"Modèle : {HF_MODEL_ID}")
    print("Token Hugging Face : configuré (valeur masquée)")