import { useLocation } from "react-router-dom"

function Header() {
  const { pathname } = useLocation()
  const  pageTitles: Record<string, string> = {
    "/dashboard": "Dashboard",
    "/documents": "Documents",
    "/chat": "Chat",
    "/settings": "Settings",
  }
  const title = pageTitles[pathname] ?? "KnowledgeHub"
  return (
    <header className="flex justify-between items-center border-b border-border-default px-7 py-4">
      <h1 className="text-sm font-semibold text-text-primary">
        {title}
      </h1>
      <span className="text-sm text-text-primary">
        Minh Hieu
      </span>
    </header>
  )
}

export default Header