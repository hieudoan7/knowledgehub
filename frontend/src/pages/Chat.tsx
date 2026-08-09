import { useEffect, useState, type FormEvent } from "react";
import { Link, useParams } from "react-router-dom";

import {
  chatWithDocument,
  getDocument,
  type ChatResponse,
  type Document,
} from "../api/documents";

function Chat() {
  const { documentId } = useParams<{
    documentId: string;
  }>();

  const [document, setDocument] = useState<Document | null>(null);
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState<ChatResponse | null>(null);

  const [loading, setLoading] = useState(true);
  const [asking, setAsking] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadDocument = async () => {
      if (!documentId) {
        setError("Document not found.");
        setLoading(false);
        return;
      }

      try {
        const data = await getDocument(documentId);
        setDocument(data);
      } catch {
        setError("Failed to load document.");
      } finally {
        setLoading(false);
      }
    };

    loadDocument();
  }, [documentId]);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();

    if (!documentId || !question.trim()) {
      return;
    }

    setError("");
    setAsking(true);

    try {
      const data = await chatWithDocument(
        documentId,
        question.trim()
      );

      setResponse(data);
      setQuestion("");
    } catch {
      setError("Failed to get an answer.");
    } finally {
      setAsking(false);
    }
  };

  if (loading) {
    return <p>Loading document...</p>;
  }

  if (error && !document) {
    return (
      <main>
        <Link to="/documents">
          ← Back to documents
        </Link>

        <p>{error}</p>
      </main>
    );
  }

  return (
    <main>
      <header>
        <Link to="/documents">
          ← Back to documents
        </Link>

        <h1>{document?.original_filename}</h1>
      </header>

      <section>
        {response && (
          <>
            <h2>Answer</h2>

            <p>{response.answer}</p>

            <h3>Sources</h3>

            {response.sources.length === 0 ? (
              <p>No sources returned.</p>
            ) : (
              response.sources.map((source) => (
                <div key={source.chunk_index}>
                  <strong>
                    Chunk {source.chunk_index}
                  </strong>

                  {" — "}

                  Score: {source.score.toFixed(3)}
                </div>
              ))
            )}
          </>
        )}

        {!response && (
          <p>
            Ask a question about this document.
          </p>
        )}
      </section>

      {error && <p>{error}</p>}

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={(event) =>
            setQuestion(event.target.value)
          }
          placeholder="Ask a question about this document..."
          disabled={asking}
        />

        <button
          type="submit"
          disabled={asking || !question.trim()}
        >
          {asking ? "Thinking..." : "Ask"}
        </button>
      </form>
    </main>
  );
}

export default Chat;