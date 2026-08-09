import { useEffect, useState, type ChangeEvent } from "react";
import { Link } from "react-router-dom";
import {
  getDocuments,
  getDocument,
  uploadDocument,
  type Document,
} from "../api/documents";
import { useAuth } from "../context/AuthContext";

function Documents() {
  const { user, logout } = useAuth();

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
          setError("Failed to check document processing status.");
        });
      }
    } catch {
      setError("Failed to upload document.");
    } finally {
      setUploading(false);

      // Allow uploading the same file again.
      event.target.value = "";
    }
  };

  if (loading) {
    return <p>Loading documents...</p>;
  }

  return (
    <main>
      <header>
        <h1>KnowledgeHub</h1>

        <div>
          <span>
            Welcome, {user?.full_name}
          </span>

          <button onClick={logout}>
            Logout
          </button>
        </div>
      </header>

      <section>
        <h2>My Documents</h2>

        <label>
          {uploading ? "Uploading..." : "Upload Document"}

          <input
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={handleUpload}
            disabled={uploading}
            hidden
          />
        </label>

        {error && <p>{error}</p>}

        {!error && documents.length === 0 && (
          <p>
            You haven't uploaded any documents yet.
          </p>
        )}

        {documents.map((document) => (
          <article key={document.id}>
            <h3>{document.original_filename}</h3>

            <p>
              Status: {document.status}
            </p>
            {document.status === "ready" && (
              <Link
                to={`/documents/${document.id}/chat`}
              >
                Open Chat
              </Link>
            )}
            <p>
              Uploaded:{" "}
              {new Date(
                document.created_at
              ).toLocaleString()}
            </p>
          </article>
        ))}
        
      </section>
    </main>
  );
}

export default Documents;