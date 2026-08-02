from app.llm.message import ChatMessage


def build_rag_messages(
    *,
    question: str,
    context: str,
) -> list[ChatMessage]:
    """
    Build messages for Retrieval-Augmented Generation.
    """

    system_prompt = """
You are an information extraction assistant.

Your task is to extract information from the supplied document.

Rules:

- Use ONLY the supplied context.
- Never invent information.
- If the answer is not present, reply exactly:
  I don't know.

If the user asks for technologies, skills, tools, frameworks or programming languages:

- Scan EVERY chunk carefully.
- Extract ALL matching items.
- Do not stop after finding a few examples.
- Remove duplicates.
- Preserve the original spelling.
- Return the complete list.

Do not summarize unless the user explicitly asks for a summary.
"""

    user_prompt = f"""
Document Context

----------------

{context}

----------------

Question

{question}
"""

    return [
        ChatMessage(
            role="system",
            content=system_prompt.strip(),
        ),
        ChatMessage(
            role="user",
            content=user_prompt.strip(),
        ),
    ]
