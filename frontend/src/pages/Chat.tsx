import { Plus, BrainCircuit, Send, ChevronDown } from 'lucide-react'
import { useState, useEffect, useRef } from 'react'
import { useAuth } from '../context/AuthContext'
import { getDocuments, chatWithDocument } from '../api/client'
import { useLocation } from 'react-router-dom'

type ChatDocument = {
  id: string
  original_filename: string
}

type ChatMessage = {
  id: string
  role: 'user' | 'assistant'
  content: string
  sources?: {
    chunk_index: number
    score: number
  }[]
}

export default function Chat() {
  const location = useLocation()
  const documentIdFromNavigation = location.state?.documentId;

  const { accessToken } = useAuth()

  const [documents, setDocuments] = useState<ChatDocument[]>([])
  const [selectedDocumentId, setSelectedDocumentId] = useState('')
  const [, setLoadingDocuments] = useState(true)
  const [documentError, setDocumentError] = useState('')
  const [isDocumentMenuOpen, setIsDocumentMenuOpen] = useState(false)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [query, setQuery] = useState('')
  const [sending, setSending] = useState(false)
  const [chatError, setChatError] = useState('')
  const requestIdRef = useRef(0)

  useEffect(() => {
    if (!accessToken) {
      setLoadingDocuments(false)
      setDocumentError('Authentication token is unavailable')
      return
    }

    let cancelled = false

    async function loadDocuments() {
      try {
        const data: ChatDocument[] = await getDocuments(accessToken!)

        if (!cancelled) {
          setDocuments(data)

          if (data.length > 0) {
            const requestedDocument = data.find(
              (doc) => doc.id === documentIdFromNavigation
            );
            
            setSelectedDocumentId(
              requestedDocument?.id ?? data[0]?.id ?? ""
            );
          }
        }
      } catch {
        if (!cancelled) {
          setDocumentError('Failed to load documents.')
        }
      } finally {
        if (!cancelled) {
          setLoadingDocuments(false)
        }
      }
    }

    loadDocuments()

    return () => {
      cancelled = true
    }
  }, [accessToken])

  useEffect(() => {
    requestIdRef.current += 1
    setMessages([]);
  }, [selectedDocumentId]);

  async function handleSendMessage() {
    const trimmedQuery = query.trim()
  
    if (!trimmedQuery || !selectedDocumentId || !accessToken || sending) {
      return
    }
  
    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: trimmedQuery,
    }
  
    setMessages((prev) => [...prev, userMessage])
    setQuery('')
    setSending(true)
    setChatError('')
  
    try {
      const requestId = requestIdRef.current;
      const response = await chatWithDocument(
        selectedDocumentId,
        trimmedQuery,
        accessToken
      )
      if (requestId !== requestIdRef.current) {
        return;
      }
  
      const assistantMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
      }
  
      setMessages((prev) => [...prev, assistantMessage])
    } catch {
      setChatError('Failed to get an AI response. Please try again.')
    } finally {
      setSending(false)
    }
  }
  const handleNewChat = () => {
    setMessages([]);
    setChatError("");
  };

  return (
    <div className="px-10 py-8 flex flex-col gap-5">
      {/* Page header */}
      <section className="flex items-center justify-between">
        {/* Heading */}
        <div className="flex flex-col gap-2">
          <h1 className="text-4xl font-semibold leading-10 text-text-primary">
            AI Chat
          </h1>

          <p className="text-lg text-text-secondary">
            Ask questions about your documents
          </p>
        </div>

        {/* New Chat button */}
        <button
          type="button"
          className="flex items-center gap-3 rounded-lg border border-border-default bg-surface-default px-4 py-3 text-base font-medium text-text-primary hover:bg-surface-sidebar"
          onClick={handleNewChat}
        >
          <Plus className="h-5 w-5" />
          New Chat
        </button>
      </section>

      {/* Document selector */}
      <div className="flex items-center gap-3">
        <label
          htmlFor="chat-document"
          className="text-sm font-medium text-text-primary"
        >
          Chat with document:
        </label>

        <div className="relative w-72">
          {/* Dropdown trigger */}
          <button
            type="button"
            onClick={() =>
              setIsDocumentMenuOpen((prev) => !prev)
            }
            className="flex w-full items-center justify-between rounded-xl border border-border-default bg-surface-default px-3 py-2.5 text-sm text-text-primary"
          >
            <span className="truncate">
              {documents.find(
                (doc) => doc.id === selectedDocumentId
              )?.original_filename ?? 'Select a document'}
            </span>

            <ChevronDown className="h-4 w-4 shrink-0" />
          </button>

          {/* Dropdown options */}
          {isDocumentMenuOpen && (
            <div className="absolute left-0 top-full z-20 mt-2 w-full rounded-xl border border-border-default bg-surface-default p-1 shadow-lg">
              {documents.map((document) => (
                <button
                  key={document.id}
                  type="button"
                  onClick={() => {
                    setSelectedDocumentId(document.id)
                    setIsDocumentMenuOpen(false)
                  }}
                  className="flex w-full items-center rounded-lg px-3 py-2 text-left text-sm text-text-primary hover:bg-surface-sidebar"
                >
                  <span className="truncate">
                    {document.original_filename}
                  </span>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {documentError && (
        <p className="text-sm text-red-600">
          {documentError}
        </p>
      )}

      {/* Chat container */}
      <section className="flex h-[calc(100vh-220px)] min-h-[560px] flex-col rounded-2xl border border-border-default bg-surface-default p-3">

        {/* Conversation area */}
        <div className="flex-1 p-6">
          {messages.map((message) => (
            <div key={message.id}>
              {message.role === "user" ? (
                // User message
                <div className="flex justify-end">
                  <div className="max-w-[75%] rounded-lg bg-brand-primary px-4 py-3 text-text-on-brand">
                    {message.content}
                  </div>
                </div>
              ) : (
                // AI response
                <div className="flex justify-start items-center gap-2">
                  <BrainCircuit className='h-5 w-5 text-text-primary'/>
                  <div className="max-w-[75%] rounded-lg bg-surface-sidebar px-4 py-3 text-text-primary">
                    {message.content}
                  </div>
                </div>
              )}
            </div>
          ))}
          {chatError && (
            <div
              role="alert"
              className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
            >
              {chatError}
            </div>
          )}
          {sending && (
            <div className="flex justify-start">
              <div className="rounded-lg bg-surface-sidebar px-4 py-3">
                <p className="text-sm text-text-secondary animate-pulse">
                  AI is thinking...
                </p>
              </div>
            </div>
          )
          }
        </div>

        {/* Message input area */}
        <div className="border-t border-border-default p-3">
          <div className="flex items-center rounded-lg border border-border-default px-3">

            <input
              type="text"
              placeholder="Ask a question about your documents..."
              className="h-11 min-w-0 flex-1 bg-transparent text-sm text-text-primary outline-none placeholder:text-text-secondary"
              value={query}
              onChange={(e)=>setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage();
                }
              }}
            />

            <button
              type="button"
              aria-label="Send message"
              className="flex h-9 w-9 shrink-0 items-center justify-center text-brand-primary"
              disabled={!query.trim() || sending || !selectedDocumentId}
              onClick={handleSendMessage}
            >
              <Send className="h-5 w-5" />
            </button>

          </div>
        </div>
      </section>

    </div>
  )
}