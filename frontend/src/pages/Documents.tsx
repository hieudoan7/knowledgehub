import { Search, SlidersHorizontal, FileText, Plus } from 'lucide-react'
import { useState, useEffect, useRef } from 'react'
import { useAuth } from '../context/AuthContext'
import { getDocuments, uploadDocument, getDocumentStatus } from '../api/client'
import { useNavigate } from 'react-router-dom'

type ApiDocument = {
  id: string
  original_filename: string
  mime_type: string
  file_size: number
  status: string
  created_at: string
}

function formatFileSize(bytes: number) {
  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`
  }

  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

function formatFileType(mimeType: string) {
  const types: Record<string, string> = {
    'application/pdf': 'PDF',
    'text/plain': 'TXT',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'DOCX',
  }

  return types[mimeType] ?? mimeType
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString()
}

export default function Documents() {
  const navigate = useNavigate()
  const [search, setSearch] = useState('')
  const { accessToken } = useAuth()
  const [documents, setDocuments] = useState<ApiDocument[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [uploading, setUploading] = useState(false)
  const [uploadError, setUploadError] = useState('')
  const [uploadSuccess, setUploadSuccess] = useState('')

  useEffect(()=> {
    if (!accessToken) {
      setLoading(false)
      setError('Authentication token is unavailable')
      return
    }
    let cancelled = false
    async function loadDocuments() {
      try {
        setLoading(true)
        setError('')

        const data: ApiDocument[] = await getDocuments(accessToken!)

        if (!cancelled) {
          setDocuments(data)
        }
      } catch {
        if (!cancelled) {
          setError("Failed to load documents.")
        }
      } finally {
        if(!cancelled) {
          setLoading(false)
        }
      }
    }

    loadDocuments()

    return () => {
      cancelled = true;
    }
  }, [accessToken])

  useEffect(() => {
    if (!accessToken) return;
  
    const pendingDocuments = documents.filter(
      (doc) =>
        !["ready", "failed"].includes(
          doc.status.toLowerCase()
        )
    );
  
    // No need to poll if all documents are finished.
    if (pendingDocuments.length === 0) return;
  
    const intervalId = setInterval(async () => {
      await Promise.all(
        pendingDocuments.map(async (doc) => {
          try {
            const result = await getDocumentStatus(
              doc.id,
              accessToken
            );
  
            setDocuments((prev) =>
              prev.map((item) =>
                item.id === result.id
                  ? { ...item, status: result.status }
                  : item
              )
            );
          } catch (error) {
            // A failed status check shouldn't break polling.
            console.error(
              `Failed to fetch status for document ${doc.id}`
            );
          }
        })
      );
    }, 3000);
  
    return () => clearInterval(intervalId);
  }, [documents, accessToken]);

  const filteredDocuments = documents.filter(
    (document) => document.original_filename.toLowerCase().includes(search.toLowerCase())
  )

  async function handleFileChange(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    const file = event.target.files?.[0]
    if (!file || !accessToken) return
    setUploading(true)
    setUploadError('')
    setUploadSuccess('')
    try {
      await uploadDocument(file, accessToken)

      setUploadSuccess('Document uploaded successfully.')
      const updateDocuments: ApiDocument[] = await getDocuments(accessToken)
      setDocuments(updateDocuments)
    } catch {
      setUploadError(
        'Upload may have succeeded, but something went wrong. Please refresh the document list.'
      )
    } finally {
      setUploading(false)
      event.target.value = ''
    }
  }

  const handleDocumentClick = (documentId: string) => {
    navigate("/chat", {
      state: {
        documentId,
      },
    });
  };

  return (
    <div className="px-8 py-10 flex flex-col gap-3">
      {/* page heading */}
      <section className="flex items-center justify-between">
        <div className="flex flex-col gap-2">
          <h2 className="text-4xl font-semibold leading-10 text-text-primary">
            Documents
          </h2>
          <p className="text-base font-regular text-text-secondary">
            Manage and search your uploaded documents.
          </p>
        </div>
        <button 
          type="button"
          className="flex items-center rounded-lg bg-brand-primary px-4 py-3 text-sm font-medium text-text-on-brand gap-2"
          disabled={uploading}
          onClick={()=>fileInputRef.current?.click()}
        >
          <Plus className='h-5 w-5 text-text-on-brand'/>
          Upload Document
        </button>
        <input
          ref={fileInputRef}
          type="file"
          className='hidden'
          onChange={handleFileChange}
        />
      </section>

      {uploadError && (
        <p className="text-sm text-red-600">
          {uploadError}
        </p>
      )}

      {uploadSuccess && (
        <p className="text-sm text-success-text">
          {uploadSuccess}
        </p>
      )}
      
      {/* Search bar */}
      <div className='flex justify-between gap-3'>
        <div className='relative flex-1'>
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-text-secondary" />
          <input
            type="text"
            placeholder='Search documents ...'
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            className="h-9 w-full rounded-lg border border-border-default bg-surface-default pl-9 pr-4 text-sm text-text-primary outline-none focus:border-brand-primary focus:ring-1 focus:ring-brand-primary"
          />
        </div>

        <button 
          type="button"
          aria-lable="Toggle document filters"
          className='flex h-9 w-9 items-center justify-center rounded-lg border border-border-default bg-surface-default
           text-text-secondary hover:bg-surface-sidebar'>
          <SlidersHorizontal className='h-6 w-6' />
        </button>
      
      </div>

      {/* Table section */}
      <section>
      <div className="flex items-center px-3 pb-4 text-xs text-text-secondary">
        <span className="flex-1">Name</span>
        <span className="w-28">Type</span>
        <span className="w-28">Size</span>
        <span className="w-41">Uploaded</span>
        <span className="w-20">Status</span>
      </div>
        
        {/* Document rows */}
        <div className="flex flex-col gap-2">
          {loading ? (
            <p className="py-8 text-center text-sm text-text-secondary">
              Loading documents...
            </p>
          ) : error ? (
            <p className="py-8 text-center text-sm text-text-secondary">
              {error}
            </p>
          ) : filteredDocuments.length === 0 ? (
            <p className="py-8 text-center text-sm text-text-secondary">
              No documents found.
            </p>
          ) : (
            filteredDocuments.map((document) => (
              <div
                key={document.id}
                className="flex items-center rounded-lg border border-border-default px-3 py-3 
                hover:border-brand-primary cursor-pointer transition-colors duration-200"
                onClick={()=> handleDocumentClick(document.id)}
              >
                {/* Name */}
                <div className="flex min-w-0 flex-1 items-center gap-3">
                  <FileText className="h-5 w-5 shrink-0 text-text-secondary" />
              
                  <div className="flex min-w-0 flex-col">
                    <span className="truncate text-sm font-medium text-text-primary">
                      {document.original_filename}
                    </span>
                  </div>
                </div>
              
                {/* Type */}
                <span className="w-28 shrink-0 text-sm text-text-primary">
                  {formatFileType(document.mime_type)}
                </span>
              
                {/* Size */}
                <span className="w-28 shrink-0 text-sm text-text-primary">
                  {formatFileSize(document.file_size)}
                </span>
              
                {/* Uploaded */}
                <span className="w-41 shrink-0 text-sm text-text-primary">
                  {formatDate(document.created_at)}
                </span>
              
                {/* Status */}
                <span className="w-20 shrink-0">
                  <span className="inline-flex rounded-full bg-success-subtle px-2 py-1 text-xs font-medium text-success-text">
                    {document.status}
                  </span>
                </span>
              </div>
            ))
          )}
        </div>
      </section>

      {/* Document count */}
      <div className="flex items-center justify-between px-3 py-4">
        <span className="text-sm text-text-secondary">
          Showing {filteredDocuments.length === 0 ? 0 : 1}
          {'–'}
          {filteredDocuments.length} of {documents.length} documents
        </span>
      </div>
    </div>
  )
}