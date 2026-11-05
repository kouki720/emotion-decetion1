
from src.prompts.sentiment_prompt import sentiment_prompt


def test_sentiment_prompt():

    messages = sentiment_prompt.format_messages(
        text="J'adore ce produit, il est vraiment excellent !"
    )

    assert len(messages) == 2
    assert messages[0].type == "system"
    assert messages[1].type == "human"

    assert "J'adore ce produit" in messages[1].content

    print("Prompt Template créé correctement !")
    print("\n--- SYSTEM PROMPT ---")
    print(messages[0].content)

    print("\n--- HUMAN PROMPT ---")
    print(messages[1].content)


if __name__ == "__main__":
    test_sentiment_prompt()
