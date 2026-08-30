import { useState } from "react";
import type { FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/useAuth";

function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();

    setError("");
    setSubmitting(true);

    try {
      await login({
        email,
        password,
      });

      navigate("/documents");
    } catch {
      setError("Invalid email or password.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-50 px-4">
      <div className="w-full max-w-md">
        {/* Brand */}
        <div className="mb-8 text-center">
          <Link
            to="/login"
            className="text-2xl font-bold tracking-tight text-slate-900"
          >
            KnowledgeHub
          </Link>

          <p className="mt-2 text-sm text-slate-500">
            Ask questions about your documents with AI.
          </p>
        </div>

        {/* Login card */}
        <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-slate-900">
              Welcome back
            </h1>

            <p className="mt-1 text-sm text-slate-500">
              Sign in to continue to your documents.
            </p>
          </div>

          <form
            onSubmit={handleSubmit}
            className="space-y-5"
          >
            <div>
              <label
                htmlFor="email"
                className="mb-2 block text-sm font-medium text-slate-700"
              >
                Email
              </label>

              <input
                id="email"
                type="email"
                value={email}
                onChange={(event) =>
                  setEmail(event.target.value)
                }
                placeholder="you@example.com"
                autoComplete="email"
                required
                className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2.5 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-slate-500 focus:ring-2 focus:ring-slate-100"
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="mb-2 block text-sm font-medium text-slate-700"
              >
                Password
              </label>

              <input
                id="password"
                type="password"
                value={password}
                onChange={(event) =>
                  setPassword(event.target.value)
                }
                placeholder="Enter your password"
                autoComplete="current-password"
                required
                className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2.5 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-slate-500 focus:ring-2 focus:ring-slate-100"
              />
            </div>

            {error && (
              <div
                role="alert"
                className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
              >
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={submitting}
              className="w-full rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300"
            >
              {submitting ? "Signing in..." : "Sign in"}
            </button>

            <div className="my-6 flex items-center gap-3">
              <div className="h-px flex-1 bg-slate-200" />
              <span className="text-xs text-slate-400">OR</span>
              <div className="h-px flex-1 bg-slate-200" />
            </div>
            
            <button
              type="button"
              onClick={() => {
                window.location.href =
                  "http://localhost:8000/api/v1/auth/google";
              }}
              className="w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
            >
              Continue with Google
            </button>
          </form>

          <div className="mt-6 border-t border-slate-100 pt-6 text-center">
            <p className="text-sm text-slate-500">
              Don't have an account?{" "}
              <Link
                to="/register"
                className="font-medium text-slate-900 hover:underline"
              >
                Create an account
              </Link>
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}

export default Login;