import { Navigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"

function OAuthCallback() {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-sm text-text-secondary">
          Signing you in...
        </p>
      </div>
    )
  }

  if (user) {
    return <Navigate to="/dashboard" replace />
  }

  return <Navigate to="/login" replace />
}

export default OAuthCallback
