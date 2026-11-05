
from src.pipelines.sentiment_pipeline import analyze_sentiment


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
    }
]


def run_pipeline_tests():

    successful = 0
    failed = 0
    category_matches = 0

    print("\n==============================================")
    print("          SENTIMENT PIPELINE TESTS")
    print("==============================================")

    for index, test_case in enumerate(TEST_CASES, start=1):

        text = test_case["text"]
        expected = test_case["expected"]

        print(f"\n\nTEST {index}/{len(TEST_CASES)}")
        print("-" * 50)
        print(f"Texte : {text}")
        print(f"Sentiment attendu : {expected}")

        try:
            result = analyze_sentiment(text)

            actual = result.sentiment

            print("\nRésultat obtenu :")
            print(result.model_dump_json(indent=4))

            successful += 1

            if actual == expected:
                category_matches += 1
                print("\nVERIFICATION : CORRECT")
            else:
                print(f"\nVERIFICATION : DIFFERENT (obtenu : {actual})")

        except Exception as error:

            failed += 1

            print("\nTEST FAILED")
            print(f"{type(error).__name__}: {error}")

    total = len(TEST_CASES)

    print("\n\n==============================================")
    print("                TEST SUMMARY")
    print("==============================================")

    print(f"Total des tests       : {total}")
    print(f"Exécutions réussies   : {successful}")
    print(f"Échecs techniques     : {failed}")
    print(f"Sentiments correspondants : {category_matches}/{total}")

    if successful:
        print(
            f"Taux de correspondance : "
            f"{category_matches / successful * 100:.2f}%"
        )

    print("==============================================")


if __name__ == "__main__":
    run_pipeline_tests()
