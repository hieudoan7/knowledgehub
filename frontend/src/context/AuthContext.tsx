import { createContext, useContext, useState, useEffect } from "react";
import { refresh, getCurrentUser, logout as logoutApi } from "../api/client";

type User = {
    email: string;
};

type AuthContextType = {
    user: User | null;
    accessToken: string | null;
    loading: boolean;
    setUser: (user: User | null) => void;
    setAccessToken: (token: string | null) => void;
    logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | undefined>(
    undefined
);

export function AuthProvider({
    children,
}: {
    children: React.ReactNode;
}) {
    const [user, setUser] = useState<User | null>(null);
    const [accessToken, setAccessToken] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);

    async function checkAuth() {
        try {
            const refreshResponse = await refresh();
            const { access_token } = refreshResponse;

            const currentUser = await getCurrentUser(access_token);

            setAccessToken(access_token);
            setUser(currentUser);
        } catch {
            setAccessToken(null);
            setUser(null);
        } finally {
            setLoading(false);
        }
    }

    async function logout() {
        await logoutApi();
    
        setAccessToken(null);
        setUser(null);
    }

    useEffect(() => {
        checkAuth();
    }, []);

    return (
        <AuthContext.Provider
            value={{
                user,
                accessToken,
                loading,
                setUser,
                setAccessToken,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);

    if (!context) {
        throw new Error("useAuth must be used inside AuthProvider");
    }

    return context;
}