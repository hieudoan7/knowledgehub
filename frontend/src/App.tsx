import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";
import AppLayout from "./layouts/AppLayout";
import ProtectedRoute from "./components/ProtectedRoute";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Documents from "./pages/Documents";
import Chat from "./pages/Chat";
import OAuthCallback from "./pages/OAuthCallback";

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/oauth/callback" element={<OAuthCallback />} />

          {/* Authenticated application */}
          <Route element={<ProtectedRoute />}>
            <Route element={<AppLayout />}>
              <Route
                path="/documents"
                element={<Documents />}
              />

              <Route
                path="/documents/:documentId/chat"
                element={<Chat />}
              />
            </Route>
          </Route>

          {/* Default route */}
          <Route
            path="/"
            element={<Navigate to="/login" replace />}
          />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;