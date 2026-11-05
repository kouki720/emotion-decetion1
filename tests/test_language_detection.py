
from src.tools.language_detection import detect_language


def test_french_detection():
    result = detect_language.invoke({
        "text": "Bonjour, je suis très satisfait de ce produit."
    })

    assert result["language_code"] == "fr"
    print("French detection:", result)


def test_english_detection():
    result = detect_language.invoke({
        "text": "Hello, I am very happy with this product."
    })

    assert result["language_code"] == "en"
    print("English detection:", result)


def test_arabic_detection():
    result = detect_language.invoke({
        "text": "أنا سعيد جدا بهذا المنتج وأحب استخدامه."
    })

    assert result["language_code"] == "ar"
    print("Arabic detection:", result)


def test_empty_text():
    try:
        detect_language.invoke({"text": ""})
        assert False, "Une erreur était attendue."
    except ValueError:
        print("Empty text validation: OK")


if __name__ == "__main__":
    test_french_detection()
    test_english_detection()
    test_arabic_detection()
    test_empty_text()

    print("\nTous les tests sont réussis !")
