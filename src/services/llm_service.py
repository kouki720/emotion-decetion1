from langchain_huggingface import (
    ChatHuggingFace,
    HuggingFaceEndpoint,
)

from src.config.settings import (
    HF_TOKEN,
    HF_MODEL_ID,
    validate_settings,
)


def get_llm():
    """
    Initialise et retourne le modèle Qwen via Hugging Face API.
    """

    validate_settings()

    endpoint = HuggingFaceEndpoint(
        repo_id=HF_MODEL_ID,
        provider="featherless-ai",
        task="text-generation",
        huggingfacehub_api_token=HF_TOKEN,
        max_new_tokens=128,
        do_sample=False,
        timeout=120,
    )

    chat_model = ChatHuggingFace(
        llm=endpoint
    )

    return chat_model


if __name__ == "__main__":

    print("Initialisation du modèle...")

    llm = get_llm()

    print("Envoi du premier message à Qwen...")

    response = llm.invoke(
        "Explique en deux phrases ce qu'est l'analyse de sentiment."
    )

    print("\nRéponse du modèle :")
    print(response.content)