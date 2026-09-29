import {ChevronRight, MessageCircle} from 'lucide-react';

type ConversationRowProps = {
	title: string,
	time: string,
  onClick?: () => void,
}

function ConversationRow({
	title,
	time,
  onClick,
}: ConversationRowProps) {
  return (
    <div 
      className="flex cursor-pointer items-center justify-between rounded-lg border border-border-default bg-surface-default px-4 py-3"
      onClick={onClick}
    >
      <div className="flex items-center gap-4">
        <MessageCircle className="h-5 w-5 text-text-secondary" />

        <div className="flex flex-col gap-1">
          <span className="text-sm font-medium text-text-primary">
            {title}
          </span>

          <span className="text-sm text-text-secondary">
            AI Chat · {time}
          </span>
        </div>
      </div>

      <ChevronRight className="h-5 w-5 text-text-secondary" />
    </div>
  )
}

export default ConversationRow