from app.llm.message import ChatMessage
from app.llm.factory import get_llm_service


def main() -> None:
    llm = get_llm_service()

    messages = [
        ChatMessage(
            role="system",
            content=(
                "You are a helpful assistant. "
                "Answer ONLY using the information provided by the user. "
                "If the answer cannot be determined, say 'I don't know.'"
            ),
        ),
        ChatMessage(
            role="user",
            content=(
                "Context:\n"
                "Python is a programming language.\n\n"
                "Question:\n"
                "What language is mentioned?"
            ),
        ),
    ]

    answer = llm.generate(messages=messages)

    print("=" * 60)
    print(answer)
    print("=" * 60)


if __name__ == "__main__":
    main()
