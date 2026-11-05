
from functools import lru_cache

from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config.settings import GOOGLE_API_KEY, validate_settings


REQUEST_TIMEOUT = 45

ACTIVE_MODEL_ID = None
UNAVAILABLE_MODELS = set()


def normalize_model_name(model_name: str) -> str:
    return model_name.split("/")[-1]


@lru_cache(maxsize=1)
def get_available_models() -> tuple:

    validate_settings()

    client = genai.Client(api_key=GOOGLE_API_KEY)

    available_models = []

    for model in client.models.list():

        supported_actions = (
            getattr(model, "supported_actions", None)
            or getattr(model, "supported_generation_methods", None)
            or []
        )

        if "generateContent" not in supported_actions:
            continue

        model_name = normalize_model_name(model.name)

        if (
            model_name.startswith("gemini-")
            and model_name not in available_models
        ):
            available_models.append(model_name)

    if not available_models:
        raise RuntimeError(
            "Aucun modèle Gemini compatible n'est accessible."
        )

    return tuple(available_models)


def create_model(model_id: str):

    return ChatGoogleGenerativeAI(
        model=model_id,
        google_api_key=GOOGLE_API_KEY,
        temperature=0,
        max_output_tokens=512,
        timeout=REQUEST_TIMEOUT,
        max_retries=0,
    )


def get_active_model_id():
    return ACTIVE_MODEL_ID


def set_active_model_id(model_id: str):

    global ACTIVE_MODEL_ID

    ACTIVE_MODEL_ID = model_id


def mark_model_unavailable(model_id: str):

    UNAVAILABLE_MODELS.add(model_id)

    global ACTIVE_MODEL_ID

    if ACTIVE_MODEL_ID == model_id:
        ACTIVE_MODEL_ID = None


def get_candidate_models():

    available_models = get_available_models()

    candidates = []

    # 1. Essayer d'abord le modèle qui a déjà fonctionné.
    if ACTIVE_MODEL_ID and ACTIVE_MODEL_ID not in UNAVAILABLE_MODELS:
        candidates.append(ACTIVE_MODEL_ID)

    # 2. Ajouter les autres modèles non encore déclarés indisponibles.
    for model_id in available_models:

        if (
            model_id not in UNAVAILABLE_MODELS
            and model_id not in candidates
        ):
            candidates.append(model_id)

    return candidates


if __name__ == "__main__":

    try:
        models = get_available_models()

        print(f"Nombre de modèles accessibles : {len(models)}")

        if ACTIVE_MODEL_ID:
            print(f"Modèle actif : {ACTIVE_MODEL_ID}")

    except Exception as error:
        print(f"Erreur : {type(error).__name__}: {error}")
