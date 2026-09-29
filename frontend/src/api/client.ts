const API_BASE_URL = "https://3-24-24-18.sslip.io/api/v1"

export async function login(email: string, password: string){
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
            email,
            password,
        }),
    });
    if (!response.ok) {
        const error = await response.json();
        console.error("Login error: ", error);
        throw new Error("Login failed");
    }

    return response.json();
}

export async function refresh() {
    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: "POST",
        credentials: "include",
    });
    if (!response.ok) {
        throw new Error("Refresh failed");
    }
    return response.json();
}

export async function getCurrentUser(accessToken: string) {
    const response = await fetch(`${API_BASE_URL}/users/me`, {
        method: "GET",
        credentials: "include",
        headers: {
            Authorization: `Bearer ${accessToken}`,
        }
    });
    if (!response.ok) {
        throw new Error("Failed to get curretn user");
    }
    return response.json();
}

export async function getDocuments(accessToken: string) {
    const response = await fetch(`${API_BASE_URL}/documents`, {
        method: "GET",
        credentials: "include",
        headers: {
            Authorization: `Bearer ${accessToken}`,
        }
    });
    if (!response.ok) {
        throw new Error("Failed to fetch documents");
    }
    return response.json();
}

export async function uploadDocument(
    file: File,
    accessToken: string
) {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch(`${API_BASE_URL}/documents/upload`, {
        method: "POST",
        headers: {
            Authorization: `Bearer ${accessToken}`,
        },
        credentials: "include",
        body: formData,
    })
    if (!response.ok) {
        const error = await response.json()
        throw new Error(
            error.detail || "Failed to upload document"
        )
    }
    return response.json()
}

type ChatSource = {
    chunk_index: number
    score: number
  }
  
type ChatResponse = {
    answer: string
    sources: ChatSource[]
}

export async function chatWithDocument(
    documentId: string,
    query: string,
    accessToken: string
): Promise<ChatResponse> {
    const response = await fetch(
        `${API_BASE_URL}/documents/${documentId}/chat`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${accessToken}`,
            },
            credentials: 'include',
            body: JSON.stringify({ question: query }),
        }
    )

    if (!response.ok) {
        throw new Error('Failed to get AI response')
    }

    return response.json()
}

export type DocumentStatus = {
    id: string;
    status: string;
  };


export async function getDocumentStatus(
    documentId: string,
    accessToken: string
): Promise<DocumentStatus> {
    const response = await fetch(
    `${API_BASE_URL}/documents/${documentId}/status`,
    {
    method: "GET",
    headers: {
        Authorization: `Bearer ${accessToken}`,
    },
    credentials: "include",
    }
    );

    if (!response.ok) {
    throw new Error("Failed to fetch document status");
    }

    return response.json();
}

export type Document = {
    id: string;
    owner_id: string;
    original_filename: string;
    stored_filename: string;
    mime_type: string;
    file_size: number;
    storage_path: string;
    status: string;
    extracted_text: string | null;
    created_at: string;
    updated_at: string;
};

export type ChatHistoryItem = {
    id: string;
    document_id: string;
    question: string;
    answer: string;
    sources: ChatSource[];
    created_at: string;
};

export type DashboardStats = {
    total_documents: number;
    ready_documents: number;
    total_chats: number;
    chats_this_week: number;
};

export type DashboardResponse = {
    stats: DashboardStats;
    recent_documents: Document[];
    recent_chats: ChatHistoryItem[];
};

export async function getDashboard(
    accessToken: string
): Promise<DashboardResponse> {
    const response = await fetch(
        `${API_BASE_URL}/dashboard`,
        {
            method: "GET",
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
            credentials: "include",
        }
    );

    if (!response.ok) {
        throw new Error("Failed to fetch dashboard");
    }

    return response.json();
}