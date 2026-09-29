import { NavLink } from 'react-router-dom'

import {
  LayoutDashboard,
  FileText,
  MessageSquare,
  Settings,
} from 'lucide-react'


function Sidebar() {
  return (
    <aside className="flex h-screen shrink-0 flex-col w-60 bg-surface-sidebar p-6">
      {/* Top section */}
      <div>
        {/* Logo */}
        <div className="text-lg font-semibold text-text-primary">
          KnowledgeHub
        </div>

        {/* Main navigation */}
        <nav className="mt-6 flex flex-col gap-2">
          <NavLink 
            to="/dashboard"
            className={({isActive}) => `flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium ${
              isActive? 'bg-brand-subtle text-text-primary': 'text-text-secondary'
            }`}
          >
            <LayoutDashboard className='h-4 w-4' />
            Dashboard
          </NavLink>

          <NavLink
            to="/documents"
            className={
              ({isActive}) => `flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium 
              ${isActive? 'bg-brand-subtle text-text-primary': 'text-text-secondary'}`
            }
          >
            <FileText className="h-4 w-4" />
            Documents
          </NavLink>

          <NavLink
            to="/chat"
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium ${
                isActive
                  ? 'bg-brand-subtle text-text-primary'
                  : 'text-text-secondary'
              }`
            }
          >
            <MessageSquare className="h-4 w-4" />
            AI Chat
          </NavLink>
        </nav>
      </div>

      {/* Bottom navigation */}
      <div className="mt-auto">
        <div className="border-t border-border-default pt-4">
        <NavLink
          to="/settings"
          className={({ isActive }) =>
            `flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium ${
              isActive
                ? 'bg-brand-subtle text-text-primary'
                : 'text-text-secondary'
            }`
          }
        >
          <Settings className="h-4 w-4" />
          Settings
        </NavLink>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar