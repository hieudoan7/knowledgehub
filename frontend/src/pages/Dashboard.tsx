import { useEffect, useState } from "react";
import { FileText, MessageCircle } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { getDashboard, type DashboardResponse } from "../api/client";
import { formatFileSize, formatFileType, formatRelativeTime } from "../utils/format";
import { useAuth } from "../context/AuthContext";

import StatCard from "../components/dashboard/StatCard";
import DocumentRow from "../components/dashboard/DocumentRow";
import ConversationRow from "../components/dashboard/ConversationRow";

export default function Dashboard() {
  const navigate = useNavigate()
  const { accessToken } = useAuth();

  const [dashboard, setDashboard] = useState<DashboardResponse | null>(null);

  useEffect(() => {
    if (!accessToken) {
      return;
    }

    async function fetchDashboard() {
      try {
        const data = await getDashboard(accessToken!);
        setDashboard(data);
      } catch (error) {
        console.error("Failed to load dashboard:", error);
      }
    }

    fetchDashboard();
  }, [accessToken]);

  return (
    <div className="flex flex-col gap-8 px-10 py-8">       
      {/* Welcome Section */}
      <section className="flex flex-col gap-2">
        <h1 className="text-4xl font-semibold leading-10 text-text-primary">
          Good day, mate 👋
        </h1>
        <p className="text-base text-text-secondary">
          Here's what's happening with your knowledge base.
        </p>
      </section>
      {/* Stats Section */}
      <section className="flex gap-4">
        <StatCard
          icon={FileText}
          label="Documents"
          value={dashboard?.stats.total_documents ?? 0}
        />

        <StatCard
          icon={FileText}
          label="Ready Documents"
          value={dashboard?.stats.ready_documents ?? 0}
        />

        <StatCard
          icon={MessageCircle}
          label="Total Chats"
          value={dashboard?.stats.total_chats ?? 0}
        />

        <StatCard
          icon={MessageCircle}
          label="Chats This Week"
          value={dashboard?.stats.chats_this_week ?? 0}
        />
      </section>

      {/* Recent Document Section */}
      <div>
        <div className="flex justify-between">
          <h2 className="text-lg font-semibold text-text-primary">
            Recent Documents
          </h2>
          <button
            className="text-sm font-medium text-text-secondary transition-colors duration-200 hover:text-text-primary cursor-pointer"
            onClick={() => navigate("/documents")}
          >
            View all
          </button>
        </div>
        <div className="mt-2 flex flex-col gap-3">
          {dashboard?.recent_documents.map((document) => (
            <DocumentRow
              key={document.id}
              name={document.original_filename}
              type={formatFileType(document.mime_type)}
              size={formatFileSize(document.file_size)}
              uploadedAt={formatRelativeTime(document.created_at)}
              status={document.status}
              onClick={() => navigate("/chat", {
                state: { documentId: document.id}
              })}
            />
          ))}
        </div>
      </div>

      {/* Recent AI Chats */}
      <div>
        <div className="flex justify-between">
          <h2 className="text-lg font-semibold text-text-primary">
            Recent AI Chats
          </h2>
          <button
            onClick={() => navigate("/chat")}
            className="text-sm font-medium text-text-secondary transition-colors duration-200 hover:text-text-primary cursor-pointer"
          >
            View all
          </button>
        </div>
        <div className="mt-2 flex flex-col gap-3">
          {dashboard?.recent_chats.map((chat) => (
            <ConversationRow
              key={chat.id}
              title={chat.question}
              time={formatRelativeTime(chat.created_at)}
              onClick={() => 
                navigate("/chat", {
                  state: { documentId: chat.document_id},
                })
              }
            />
          ))}
        </div>
      </div>
    </div>
  )
}