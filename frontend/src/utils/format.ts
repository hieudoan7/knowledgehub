export function formatFileSize(bytes: number): string {
  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`
  }

  return `${(bytes / 1024 / 1024).toFixed(1)} MB`
}

export function formatFileType(mimeType: string): string {
  const types: Record<string, string> = {
    "application/pdf": "PDF",
    "text/plain": "TXT",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
      "DOCX",
  }

  return types[mimeType] ?? mimeType
}

export function formatRelativeTime(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()

  const diffInSeconds = Math.floor(
    (now.getTime() - date.getTime()) / 1000
  )

  if (diffInSeconds < 60) {
    return "just now"
  }

  const diffInMinutes = Math.floor(diffInSeconds / 60)

  if (diffInMinutes < 60) {
    return `${diffInMinutes} minute${diffInMinutes === 1 ? "" : "s"} ago`
  }

  const diffInHours = Math.floor(diffInMinutes / 60)

  if (diffInHours < 24) {
    return `${diffInHours} hour${diffInHours === 1 ? "" : "s"} ago`
  }

  const diffInDays = Math.floor(diffInHours / 24)

  if (diffInDays < 7) {
    return `${diffInDays} day${diffInDays === 1 ? "" : "s"} ago`
  }

  const diffInWeeks = Math.floor(diffInDays / 7)

  return `${diffInWeeks} week${diffInWeeks === 1 ? "" : "s"} ago`
}