import { useEffect, useState, useRef, type FormEvent } from "react";

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
  
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

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

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

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
    return (
      <div className="flex min-h-[500px] items-center justify-center">
        <p className="text-sm text-slate-500">
          Loading document...
        </p>
      </div>
    );
  }

  if (error && !document) {
    return (
      <div className="rounded-xl border border-red-200 bg-red-50 p-6">
        <Link
          to="/documents"
          className="text-sm font-medium text-slate-700 hover:text-slate-900"
        >
          ← Back to documents
        </Link>

        <p className="mt-4 text-sm text-red-700">
          {error}
        </p>
      </div>
    );
  }

  return (
    <div className="flex h-[calc(100vh-9rem)] flex-col">
      {/* Document header */}
      <div className="mb-4 flex shrink-0 items-center gap-4 border-b border-slate-200 pb-4">
        <Link
          to="/documents"
          className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-600 transition hover:bg-slate-100"
          aria-label="Back to documents"
        >
          ←
        </Link>
  
        <div className="min-w-0">
          <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
            Document
          </p>
  
          <h1 className="truncate text-lg font-bold text-slate-900">
            {document?.original_filename}
          </h1>
        </div>
      </div>
  
      {/* Conversation */}
      <section className="min-h-0 flex-1 overflow-y-auto">
        <div className="mx-auto max-w-4xl space-y-8 px-2 py-4">
          {messages.length === 0 ? (
            <div className="flex min-h-[400px] items-center justify-center">
              <div className="max-w-md text-center">
                <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-slate-900 text-2xl text-white">
                  ✦
                </div>
  
                <h2 className="text-xl font-semibold text-slate-900">
                  Ask anything about this document
                </h2>
  
                <p className="mt-2 text-sm leading-6 text-slate-500">
                  KnowledgeHub will search the document and
                  use the relevant content to generate an
                  answer.
                </p>
              </div>
            </div>
          ) : (
            messages.map((message) => (
              <article
                key={message.id}
                className="space-y-5"
              >
                {/* User question */}
                <div className="flex justify-end">
                  <div className="max-w-[75%]">
                    <div className="mb-1 text-right text-xs font-medium text-slate-400">
                      You
                    </div>
  
                    <div className="rounded-2xl rounded-tr-md bg-slate-900 px-5 py-3 text-sm leading-6 text-white">
                      {message.question}
                    </div>
                  </div>
                </div>
  
                {/* AI answer */}
                <div className="flex justify-start">
                  <div className="w-full max-w-3xl">
                    <div className="mb-2 flex items-center gap-2 text-xs font-medium text-slate-400">
                      <span className="flex h-6 w-6 items-center justify-center rounded-lg bg-slate-900 text-xs text-white">
                        ✦
                      </span>
  
                      KnowledgeHub
                    </div>
  
                    <div className="rounded-2xl rounded-tl-md border border-slate-200 bg-white px-5 py-4 shadow-sm">
                      <p className="whitespace-pre-wrap text-sm leading-7 text-slate-700">
                        {message.answer}
                      </p>
  
                      {/* Sources */}
                      <div className="mt-5 border-t border-slate-100 pt-4">
                        <p className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-400">
                          Sources
                        </p>
  
                        {message.sources.length === 0 ? (
                          <p className="text-sm text-slate-400">
                            No sources returned.
                          </p>
                        ) : (
                          <div className="flex flex-wrap gap-2">
                            {message.sources.map(
                              (source, index) => (
                                <div
                                  key={`${message.id}-${source.chunk_index}-${index}`}
                                  className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2"
                                >
                                  <span className="text-xs font-medium text-slate-700">
                                    Chunk {source.chunk_index}
                                  </span>
  
                                  <span className="ml-2 text-xs text-slate-400">
                                    {source.score.toFixed(3)}
                                  </span>
                                </div>
                              )
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </article>
            ))
          )}
          <div ref={messagesEndRef} />
        </div>
      </section>
  
      {/* Error */}
      {error && (
        <div className="mx-auto mt-3 w-full max-w-4xl shrink-0 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}
  
      {/* Question input */}
      <form onSubmit={handleSubmit} className="shrink-0 border-t border-slate-200 bg-slate-50 py-4">
        <div className="mx-auto w-full max-w-4xl">
          <div className="flex items-center gap-3 rounded-xl border border-slate-300 bg-white p-2 shadow-sm focus-within:border-slate-500 focus-within:ring-2 focus-within:ring-slate-100">
            <input
              type="text"
              value={question}
              onChange={(event) =>
                setQuestion(event.target.value)
              }
              placeholder="Ask a question about this document..."
              disabled={asking}
              className="min-w-0 flex-1 bg-transparent px-3 py-2 text-sm text-slate-900 outline-none placeholder:text-slate-400"
            />
  
            <button
              type="submit"
              disabled={asking || !question.trim()}
              className="rounded-lg bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300"
            >
              {asking ? "Thinking..." : "Ask →"}
            </button>
          </div>
  
          <p className="mt-2 text-center text-xs text-slate-400">
            Answers are generated from the contents of this document.
          </p>
        </div>
      </form>
    </div>
  );
}

export default Chat;