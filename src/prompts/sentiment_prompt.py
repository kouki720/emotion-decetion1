
from langchain_core.prompts import ChatPromptTemplate

from src.prompts.system_prompt import SYSTEM_PROMPT


sentiment_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),

        (
            "human",
            """
            Analyse le texte suivant :

            <text_to_analyze>
            {text}
            </text_to_analyze>

            Retourne les résultats de ton analyse en respectant
            les règles et le schéma de sortie définis.
            """
        )
    ]
)
