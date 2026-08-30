import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../api/client";

function OAuthCallback() {
  const navigate = useNavigate();

  useEffect(() => {
    const completeLogin = async () => {
      try {
        const response = await apiClient.post("/auth/refresh");

        localStorage.setItem(
          "access_token",
          response.data.access_token,
        );

        navigate("/documents", { replace: true });
      } catch (error) {
        console.error("OAuth login failed:", error);
        navigate("/login", { replace: true });
      }
    };

    completeLogin();
  }, [navigate]);

  return (
    <main className="flex min-h-screen items-center justify-center">
      <p className="text-sm text-slate-500">
        Signing you in...
      </p>
    </main>
  );
}

export default OAuthCallback;