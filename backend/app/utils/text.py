import re


_SENTENCE_PATTERN = re.compile(r"(?<=[.!?])\s+")


def split_text(
    text: str,
    *,
    chunk_size: int,
    overlap_sentences: int,
) -> list[str]:
    """
    Split text into sentence-aware overlapping chunks.

    Sentences are kept intact whenever possible. If a sentence exceeds
    ``chunk_size``, it is further split on word boundaries.

    Args:
        text: Input text.
        chunk_size: Maximum characters per chunk.
        overlap_sentences: Number of sentences shared between
            consecutive chunks.

    Returns:
        List of text chunks.
    """

    text = " ".join(text.split())

    if not text:
        return []

    sentences = _split_sentences(text)

    chunks: list[str] = []

    current_chunk: list[str] = []
    current_length = 0

    for sentence in sentences:
        # Extremely long sentence
        if len(sentence) > chunk_size:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_length = 0

            chunks.extend(_split_long_sentence(sentence, chunk_size))
            continue

        additional = len(sentence)
        if current_chunk:
            additional += 1

        if current_length + additional <= chunk_size:
            current_chunk.append(sentence)
            current_length += additional
            continue

        chunks.append(" ".join(current_chunk))

        current_chunk = current_chunk[-overlap_sentences:]
        current_length = len(" ".join(current_chunk))

        current_chunk.append(sentence)
        current_length = len(" ".join(current_chunk))

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def _split_sentences(text: str) -> list[str]:
    """
    Split text into sentences.
    """

    return [
        sentence.strip()
        for sentence in _SENTENCE_PATTERN.split(text)
        if sentence.strip()
    ]


def _split_long_sentence(
    sentence: str,
    chunk_size: int,
) -> list[str]:
    """
    Split an overly long sentence on word boundaries.
    """

    words = sentence.split()

    chunks: list[str] = []

    current_words: list[str] = []
    current_length = 0

    for word in words:
        additional = len(word)
        if current_words:
            additional += 1

        if current_length + additional <= chunk_size:
            current_words.append(word)
            current_length += additional
            continue

        chunks.append(" ".join(current_words))

        current_words = [word]
        current_length = len(word)

    if current_words:
        chunks.append(" ".join(current_words))

    return chunks