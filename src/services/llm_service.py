
from functools import lru_cache

from langchain_google_genai import ChatGoogleGenerativeAI

from src.config.settings import (
    GOOGLE_API_KEY,
    validate_settings,
)


FREE_GEMINI_MODELS = [
    "gemini-3.6-flash",
    "gemini-3.8-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
]

ACTIVE_MODEL_ID = None

REQUEST_TIMEOUT = 45


def create_model(model_id: str):
    """Construit une instance LangChain Gemini."""

    return ChatGoogleGenerativeAI(
        model=model_id,
        google_api_key=GOOGLE_API_KEY,
        temperature=0,
        max_output_tokens=64,
        timeout=REQUEST_TIMEOUT,
        max_retries=0,
    )


@lru_cache(maxsize=1)
def get_llm():

    global ACTIVE_MODEL_ID

    validate_settings()

    test_message = (
        "Réponds brièvement : qu'est-ce que l'analyse de sentiment ?"
    )

    print("\nRecherche d'un modèle Gemini disponible...\n", flush=True)

    for model_id in FREE_GEMINI_MODELS:

        print(f"Test du modèle : {model_id}", flush=True)

        try:
            model = create_model(model_id)

            response = model.invoke(test_message)

            if not response.content:
                print("  ECHEC : réponse vide.\n", flush=True)
                continue

            ACTIVE_MODEL_ID = model_id

            print("  SUCCES : modèle disponible !", flush=True)
            print(f"  Modèle sélectionné : {model_id}\n", flush=True)

            return model

        except Exception as error:

            error_message = str(error)

            print("  ECHEC : modèle indisponible.", flush=True)
            print(
                f"  Type : {type(error).__name__}",
                flush=True
            )
            print(
                f"  Détail : {error_message[:300]}\n",
                flush=True
            )

            error_lower = error_message.lower()

            if (
                "api key not valid" in error_lower
                or "invalid api key" in error_lower
            ):
                raise RuntimeError(
                    "Clé API Gemini invalide. Vérifiez votre .env."
                ) from error

            if "permission_denied" in error_lower:
                raise RuntimeError(
                    "Accès refusé. Vérifiez les autorisations API."
                ) from error

            continue

    raise RuntimeError(
        "Aucun modèle Gemini testé n'a répondu. "
        "Vérifiez les modèles, les quotas et les autorisations."
    )


def get_active_model_id():
    return ACTIVE_MODEL_ID


if __name__ == "__main__":

    print("======================================", flush=True)
    print("       GEMINI MODEL SELECTOR", flush=True)
    print("======================================", flush=True)

    try:
        llm = get_llm()

        print("\nTEST FINAL", flush=True)

        response = llm.invoke(
            "Explique en deux phrases le fonctionnement "
            "de l'analyse de sentiment."
        )

        print("\nRéponse de Gemini :", flush=True)
        print(response.content, flush=True)

        print(
            f"\nModèle utilisé : {get_active_model_id()}",
            flush=True
        )

    except Exception as error:
        print("\nERREUR :", flush=True)
        print(error, flush=True)
