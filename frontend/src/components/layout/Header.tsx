import { useLocation, useNavigate } from "react-router-dom"
import { useAuth } from "../../context/AuthContext"

function Header() {
  const { pathname } = useLocation()
  const navigate = useNavigate()
  const { user, logout } = useAuth()

  const pageTitles: Record<string, string> = {
    "/dashboard": "Dashboard",
    "/documents": "Documents",
    "/chat": "Chat",
    "/settings": "Settings",
  }

  const title = pageTitles[pathname] ?? "KnowledgeHub"

  const handleLogout = async () => {
    await logout()
    navigate("/login")
  }

  return (
    <header className="flex items-center justify-between border-b border-border-default px-7 py-4">
      <h1 className="text-sm font-semibold text-text-primary">
        {title}
      </h1>

      <div className="flex items-center gap-4">
        <span className="text-sm text-text-primary">
          {user?.email ?? "User"}
        </span>

        <button
          type="button"
          onClick={handleLogout}
          className="rounded-md px-3 py-1.5 text-sm font-medium text-text-secondary transition-colors duration-200 hover:bg-surface-sidebar hover:text-text-primary"
        >
          Logout
        </button>
      </div>
    </header>
  )
}

export default Header