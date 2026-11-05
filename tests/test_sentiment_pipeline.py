
import json

from src.pipelines.sentiment_pipeline import analyze_sentiment

from src.tools.sentiment_statistics import (
    calculate_sentiment_statistics,
)


TEST_CASES = [
    {
        "text": "J'adore ce produit, il est vraiment excellent !",
        "expected": "very_positive"
    },
    {
        "text": "Ce service est bon et je suis satisfait.",
        "expected": "positive"
    },
    {
        "text": "Le produit est plutôt intéressant, sans être exceptionnel.",
        "expected": "slightly_positive"
    },
    {
        "text": "Le produit est correct, rien de particulier.",
        "expected": "neutral"
    },
    {
        "text": "Le service est un peu décevant.",
        "expected": "slightly_negative"
    },
    {
        "text": "Je suis très mécontent de cette expérience.",
        "expected": "negative"
    },
    {
        "text": "C'est absolument horrible, je déteste ce produit !",
        "expected": "very_negative"
    },
    {
        "text": "I really love this application, it's amazing!",
        "expected": "very_positive"
    },
    {
        "text": "هذا المنتج رائع جدا وأنا سعيد به",
        "expected": "very_positive"
    },
    {
        "text": "J'attendais mieux, mais le produit reste acceptable.",
        "expected": "slightly_negative"
    },
]


def run_tests():

    successful_results = []

    total_tests = len(TEST_CASES)
    successful_tests = 0
    failed_tests = 0
    matching_sentiments = 0

    print("\n==============================================")
    print("          SENTIMENT PIPELINE TESTS")
    print("==============================================")

    for index, test_case in enumerate(TEST_CASES, start=1):

        text = test_case["text"]
        expected = test_case["expected"]

        print(f"\nTEST {index}/{total_tests}")
        print("-" * 50)

        print(f"Texte : {text}")
        print(f"Sentiment attendu : {expected}")

        try:

            result = analyze_sentiment(text)

            successful_results.append(result)
            successful_tests += 1

            actual = result.sentiment

            print("\nRésultat obtenu :")
            print(result.model_dump_json(indent=4))

            if actual == expected:

                matching_sentiments += 1

                print("\nStatut : SUCCÈS - Sentiment correct")

            else:

                print("\nStatut : RÉUSSI - Sentiment différent de l'attendu")

        except Exception as error:

            failed_tests += 1

            print("\nStatut : ÉCHEC")
            print(f"Erreur : {type(error).__name__}: {error}")

    # ==========================================
    # TEST SUMMARY
    # ==========================================

    print("\n==============================================")
    print("                 TEST SUMMARY")
    print("==============================================")

    print(f"Total des tests       : {total_tests}")
    print(f"Analyses réussies     : {successful_tests}")
    print(f"Analyses échouées     : {failed_tests}")
    print(f"Sentiments corrects   : {matching_sentiments}")

    if successful_tests > 0:

        success_rate = successful_tests / total_tests * 100
        matching_rate = matching_sentiments / successful_tests * 100

        print(f"Taux de réussite      : {success_rate:.2f}%")
        print(f"Taux de correspondance: {matching_rate:.2f}%")

    # ==========================================
    # SENTIMENT STATISTICS
    # ==========================================

    if successful_results:

        print("\n==============================================")
        print("             SENTIMENT STATISTICS")
        print("==============================================")

        statistics = calculate_sentiment_statistics.invoke({
            "results": [
                result.model_dump()
                for result in successful_results
            ]
        })

        print(json.dumps(
            statistics,
            indent=4,
            ensure_ascii=False
        ))

    else:

        print("\nAucun résultat disponible pour calculer les statistiques.")

    print("\n==============================================")
    print("              TESTS COMPLETED")
    print("==============================================")


if __name__ == "__main__":
    run_tests()
