import { FileText } from 'lucide-react'

type DocumentRowProps = {
  name: string
	type: string
	size: string
	uploadedAt: string
	status: string
  onClick?: () => void
}

function DocumentRow({
	name,
	type,
	size,
	uploadedAt,
	status,
  onClick,
}: DocumentRowProps) {
  return (
    <div 
      className="flex cursor-pointer items-center justify-between rounded-lg border border-border-default bg-surface-default px-4 py-3"
      onClick={onClick}
    >
      <div className="flex items-center gap-4">
        <FileText className="h-5 w-5 text-text-secondary" />

        <div className="flex flex-col gap-1">
          <span className="text-sm font-medium text-text-primary">
            {name}
          </span>

          <span className="text-sm text-text-secondary">
            {type} · {size} · {uploadedAt}
          </span>
        </div>
      </div>

      <span className="rounded-full bg-success-subtle px-3 py-1 text-sm font-medium text-success-text">
        {status}
      </span>
    </div>
  )
}

export default DocumentRow