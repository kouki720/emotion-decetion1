
from src.prompts.sentiment_prompt import sentiment_prompt

from src.services.llm_service import (
    create_model,
    get_candidate_models,
    set_active_model_id,
    mark_model_unavailable,
    get_active_model_id,
)

from src.schemas.input_schema import SentimentInput
from src.schemas.sentiment_schema import SentimentResult

from src.tools.language_detection import detect_language

from src.validators.output_validator import (
    validate_sentiment_result,
)


def analyze_with_fallback(text: str) -> SentimentResult:

    candidates = get_candidate_models()
    errors = []

    for model_id in candidates:

        try:
            llm = create_model(model_id)

            structured_llm = llm.with_structured_output(
                SentimentResult,
                method="json_schema"
            )

            chain = sentiment_prompt | structured_llm

            result = chain.invoke({
                "text": text
            })

            if not isinstance(result, SentimentResult):
                raise ValueError(
                    "Réponse incompatible avec SentimentResult."
                )

            # Validation du résultat Gemini.
            validate_sentiment_result(result)

            set_active_model_id(model_id)

            print("\n========== GEMINI MODEL SELECTION ==========")
            print(f"Modèle utilisé : {get_active_model_id()}")

            return result

        except Exception as error:

            errors.append(
                f"{model_id}: {type(error).__name__}: {error}"
            )

            mark_model_unavailable(model_id)

            print(
                f"\nÉchec de {model_id}. "
                "Passage au modèle suivant..."
            )

    raise RuntimeError(
        "Aucun modèle Gemini n'a réussi l'analyse.\n"
        + "\n".join(errors)
    )


def analyze_sentiment(text: str) -> SentimentResult:

    validated_input = SentimentInput(text=text)
    text = validated_input.text

    print("\n========== SENTIMENT ANALYSIS ==========")

    sentiment_result = analyze_with_fallback(text)

    print("\n========== LANGUAGE DETECTION ==========")

    language_result = detect_language.invoke({
        "text": text
    })

    print(language_result)

    final_result = sentiment_result.model_copy(
        update={
            "language": language_result["language"]
        }
    )

    # Validation finale après ajout de la langue.
    validate_sentiment_result(final_result)

    return final_result


if __name__ == "__main__":

    test_text = "J'adore ce produit, il est vraiment excellent !"

    print("\n======================================")
    print("       SENTIMENT ANALYSIS PIPELINE")
    print("======================================")

    print(f"\nTexte analysé : {test_text}")

    try:
        result = analyze_sentiment(test_text)

        print("\n========== FINAL RESULT ==========")
        print(result.model_dump_json(indent=4))

    except Exception as error:

        print("\n========== PIPELINE ERROR ==========")
        print(f"{type(error).__name__}: {error}")
