import apiClient from "./client";

export interface Document {
  id: string;
  owner_id: string;
  original_filename: string;
  stored_filename: string;
  mime_type: string;
  file_size: number;
  storage_path: string;
  status: string;
  extracted_text?: string | null;
  created_at: string;
  updated_at: string;
}

export interface ChatSource {
  chunk_index: number;
  score: number;
}

export interface ChatResponse {
  answer: string;
  sources: ChatSource[];
}

export interface ChatHistoryItem {
  id: string;
  question: string;
  answer: string;
  sources: ChatSource[];
  created_at: string;
}

export const getDocuments = async (): Promise<Document[]> => {
  const response = await apiClient.get<Document[]>("/documents");

  return response.data;
};

export const getDocument = async (
  documentId: string
): Promise<Document> => {
  const response = await apiClient.get<Document>(
    `/documents/${documentId}`
  );

  return response.data;
};

export const deleteDocument = async (
  documentId: string
): Promise<void> => {
  await apiClient.delete(`/documents/${documentId}`);
};

export const uploadDocument = async (
  file: File
): Promise<Document> => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await apiClient.post<Document>(
    "/documents/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

export const chatWithDocument = async (
  documentId: string,
  question: string
): Promise<ChatResponse> => {
  const response = await apiClient.post<ChatResponse>(
    `/documents/${documentId}/chat`,
    { question }
  );

  return response.data;
};

export const getChatHistory = async (documentId: string): Promise<ChatHistoryItem[]> => {
  const response = await apiClient.get<ChatHistoryItem[]>(
    `/documents/${documentId}/chat/history`
  );

  return response.data;
};
