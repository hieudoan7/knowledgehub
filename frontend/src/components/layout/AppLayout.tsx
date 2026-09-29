import { Outlet } from 'react-router-dom'
import Sidebar from "./Sidebar"
import Header from "./Header"

function AppLayout() {
  return (
    <div className="min-h-screen flex">
      <Sidebar/>

      <main className="flex-1 bg-surface-default">
        <Header/>
        <Outlet/>
      </main>
    </div>
  )
}

export default AppLayout
