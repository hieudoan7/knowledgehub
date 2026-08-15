import { useEffect, useState, type ChangeEvent } from "react";
import { Link } from "react-router-dom";
import {
  getDocuments,
  getDocument,
  uploadDocument,
  type Document,
} from "../api/documents";

function Documents() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const loadDocuments = async () => {
    try {
      const data = await getDocuments();
      setDocuments(data);
    } catch {
      setError("Failed to load documents.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  const pollDocumentStatus = async (documentId: string) => {
    const maxAttempts = 30;
    const interval = 2000;

    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      const document = await getDocument(documentId);

      setDocuments((current) =>
        current.map((item) =>
          item.id === document.id ? document : item
        )
      );

      if (
        document.status === "ready" ||
        document.status === "failed"
      ) {
        return;
      }

      await new Promise((resolve) =>
        setTimeout(resolve, interval)
      );
    }
  };

  const handleUpload = async (
    event: ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setError("");
    setUploading(true);

    try {
      const document = await uploadDocument(file);

      setDocuments((current) => [
        document,
        ...current,
      ]);

      if (document.status === "uploaded") {
        pollDocumentStatus(document.id).catch(() => {
          setError(
            "Failed to check document processing status."
          );
        });
      }
    } catch {
      setError("Failed to upload document.");
    } finally {
      setUploading(false);

      event.target.value = "";
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-[400px] items-center justify-center">
        <div className="text-sm text-slate-500">
          Loading documents...
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Page heading */}
      <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">
            My Documents
          </h1>

          <p className="mt-1 text-sm text-slate-500">
            Upload documents and ask questions using AI.
          </p>
        </div>

        <label
          className={`inline-flex cursor-pointer items-center justify-center rounded-lg px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition ${
            uploading
              ? "cursor-not-allowed bg-slate-400"
              : "bg-slate-900 hover:bg-slate-800"
          }`}
        >
          {uploading ? "Uploading..." : "+ Upload Document"}

          <input
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={handleUpload}
            disabled={uploading}
            hidden
          />
        </label>
      </div>

      {/* Error */}
      {error && (
        <div className="mb-6 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Empty state */}
      {!error && documents.length === 0 && (
        <div className="rounded-xl border border-dashed border-slate-300 bg-white px-6 py-16 text-center">
          <div className="mx-auto max-w-md">
            <div className="mb-4 text-4xl">📄</div>

            <h2 className="text-lg font-semibold text-slate-900">
              No documents yet
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Upload a PDF, DOCX, or TXT file to start
              asking questions about your documents.
            </p>
          </div>
        </div>
      )}

      {/* Documents */}
      {documents.length > 0 && (
        <div className="grid gap-4">
          {documents.map((document) => (
            <article
              key={document.id}
              className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition hover:border-slate-300 hover:shadow-md"
            >
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div className="min-w-0">
                  <div className="flex items-start gap-3">
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-slate-100 text-lg">
                      📄
                    </div>

                    <div className="min-w-0">
                      <h3 className="truncate font-semibold text-slate-900">
                        {document.original_filename}
                      </h3>

                      <p className="mt-1 text-sm text-slate-500">
                        {document.mime_type} ·{" "}
                        {Math.round(
                          document.file_size / 1024
                        )}{" "}
                        KB
                      </p>

                      <p className="mt-1 text-xs text-slate-400">
                        Uploaded{" "}
                        {new Date(
                          document.created_at
                        ).toLocaleString()}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="flex shrink-0 items-center gap-3">
                  {/* Status */}
                  <span
                    className={`rounded-full px-3 py-1 text-xs font-semibold capitalize ${
                      document.status === "ready"
                        ? "bg-green-100 text-green-700"
                        : document.status === "processing"
                          ? "bg-yellow-100 text-yellow-700"
                          : document.status === "failed"
                            ? "bg-red-100 text-red-700"
                            : "bg-slate-100 text-slate-600"
                    }`}
                  >
                    {document.status}
                  </span>

                  {/* Chat */}
                  {document.status === "ready" && (
                    <Link
                      to={`/documents/${document.id}/chat`}
                      className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-800"
                    >
                      Open Chat →
                    </Link>
                  )}
                </div>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}

export default Documents;