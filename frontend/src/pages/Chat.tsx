import { useEffect, useState, type FormEvent } from "react";
import { Link, useParams } from "react-router-dom";

import {
  chatWithDocument,
  getDocument,
  getChatHistory,
  type Document,
  type ChatHistoryItem,
} from "../api/documents";

function Chat() {
  const { documentId } = useParams<{
    documentId: string;
  }>();

  const [document, setDocument] = useState<Document | null>(null);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<ChatHistoryItem[]>([]);

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
        const history = await getChatHistory(documentId);
        setMessages(history);
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
      const currentQuestion = question.trim();

      const data = await chatWithDocument(
        documentId,
        currentQuestion
      );
      
      const newMessage: ChatHistoryItem = {
        id: crypto.randomUUID(),
        question: currentQuestion,
        answer: data.answer,
        sources: data.sources,
        created_at: new Date().toISOString(),
      };
      
      setMessages((previous) => [
        ...previous,
        newMessage,
      ]);
      
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
        {messages.length === 0 ? (
          <p>Ask a question about this document.</p>
        ) : (
          messages.map((message) => (
            <article key={message.id}>
              <h3>You</h3>
              <p>{message.question}</p>

              <h3>Answer</h3>
              <p>{message.answer}</p>

              <h4>Sources</h4>

              {message.sources.length === 0 ? (
                <p>No sources returned.</p>
              ) : (
                message.sources.map((source, index) => (
                  <div key={`${message.id}-${source.chunk_index}-${index}`}>
                    <strong>
                      Chunk {source.chunk_index}
                    </strong>

                    {" — "}

                    Score: {source.score.toFixed(3)}
                  </div>
                ))
              )}

              <hr />
            </article>
          ))
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