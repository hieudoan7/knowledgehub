import { useState } from 'react'
import { ArrowRight, Eye, EyeOff } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'

import { getCurrentUser, login, register } from '../api/client'
import { useAuth } from '../context/AuthContext'

const PASSWORD_MIN_LENGTH = 8

export default function Register() {
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [isSubmiting, setIsSubmiting] = useState(false)

  const { setUser, setAccessToken } = useAuth()
  const navigate = useNavigate()

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')

    if (!email.trim()) {
      setError('Email is required.')
      return
    }

    if (!password) {
      setError('Password is required.')
      return
    }

    if (password.length < PASSWORD_MIN_LENGTH) {
      setError(`Password must be at least ${PASSWORD_MIN_LENGTH} characters.`)
      return
    }

    setIsSubmiting(true)

    try {
      await register(email.trim(), password, fullName)
      const { access_token } = await login(email.trim(), password)
      const user = await getCurrentUser(access_token)

      setAccessToken(access_token)
      setUser(user)
      navigate('/dashboard')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed.')
      console.error(err)
    } finally {
      setIsSubmiting(false)
    }
  }

  return (
    <main className="min-h-screen flex">
      <section className="w-[55%] bg-surface-sidebar flex items-center px-16">
        <div className="max-w-xl flex flex-col">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-lg bg-brand-primary" />
            <span className="text-2xl font-semibold text-text-primary">
              KnowledgeHub
            </span>
          </div>

          <h1 className="mt-12 text-4xl font-semibold text-text-primary">
            Your knowledge, intelligently connected.
          </h1>
          <p className="mt-4 text-lg text-text-secondary">
            Upload documents, search your knowledge base, and get answers powered by AI.
          </p>

          <div className="mt-12">
            <h2 className="text-lg font-semibold text-text-primary">
              Knowledge Flow
            </h2>
            <div className="mt-4 flex items-center gap-3">
              <div className="w-[180px] rounded-xl border border-border-default bg-surface-default p-5">
                <h3 className="text-lg font-semibold text-text-primary">
                  Documents
                </h3>
                <p className="mt-2 text-base text-text-secondary">
                  Upload and organize your documents.
                </p>
              </div>
              <ArrowRight className="h-5 w-5 text-brand-primary" />
              <div className="w-[180px] rounded-xl border border-border-default bg-surface-default p-5">
                <h3 className="text-lg font-semibold text-text-primary">
                  Knowledge
                </h3>
                <p className="mt-2 text-base text-text-secondary">
                  Connect and search your knowledge.
                </p>
              </div>
              <ArrowRight className="h-5 w-5 text-brand-primary" />
              <div className="w-[180px] rounded-xl border border-border-default bg-surface-default p-5">
                <h3 className="text-lg font-semibold text-text-primary">
                  AI Answer
                </h3>
                <p className="mt-2 text-base text-text-secondary">
                  Get intelligent answers from your data.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="w-[45%] bg-surface-default flex items-center jusify-center px-16">
        <form className="w-full max-w-[400px]" onSubmit={handleSubmit}>
          <div>
            <h1 className="text-[32px] font-semibold leading-10 text-text-primary">
              Create your account
            </h1>
            <p className="mt-2 text-lg leading-7 text-text-secondary">
              Sign up to start using KnowledgeHub
            </p>
          </div>

          <div className="mt-8 flex flex-col gap-6">
            <div>
              <label
                htmlFor="fullName"
                className="text-sm font-medium text-text-primary"
              >
                Full name{' '}
                <span className="font-normal text-text-secondary">(optional)</span>
              </label>
              <input
                id="fullName"
                type="text"
                placeholder="Jane Doe"
                value={fullName}
                onChange={(event) => setFullName(event.target.value)}
                disabled={isSubmiting}
                className="mt-2 w-full rounded-lg border border-border-default bg-surface-default px-4 py-3 text-base text-text-primary outline-none"
              />
            </div>

            <div>
              <label htmlFor="email" className="text-sm font-medium text-text-primary">
                Email
              </label>
              <input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                disabled={isSubmiting}
                className="mt-2 w-full rounded-lg border border-border-default bg-surface-default px-4 py-3 text-base text-text-primary outline-none"
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="text-sm font-medium text-text-primary"
              >
                Password
              </label>
              <div className="relative mt-2">
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="At least 8 characters"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  disabled={isSubmiting}
                  className="w-full rounded-lg border border-border-default bg-surface-default px-4 py-3 pr-12 text-base text-text-primary outline-none"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-text-secondary"
                >
                  {showPassword ? (
                    <EyeOff className="h-5 w-5" />
                  ) : (
                    <Eye className="h-5 w-5" />
                  )}
                </button>
              </div>
            </div>

            <div className="min-h-5">
              {error && <p className="text-sm text-error-text">{error}</p>}
            </div>

            <button
              type="submit"
              disabled={isSubmiting}
              className="w-full rounded-lg bg-brand-primary px-4 py-3 text-sm font-medium text-white transition hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-brand-primary focus:ring-offset-2"
            >
              {isSubmiting ? 'Creating account...' : 'Sign up'}
            </button>

            <p className="text-center text-sm text-text-secondary">
              Already have an account?{' '}
              <Link to="/login" className="font-medium text-brand-primary">
                Sign in
              </Link>
            </p>
          </div>
        </form>
      </section>
    </main>
  )
}
