import { createContext, useContext, useState, useEffect, useRef } from "react";
import { refresh, createGuest, getCurrentUser, logout as logoutApi } from "../api/client";

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
    const authCheckStarted = useRef(false);

    async function checkAuth() {
        try {
            const refreshResponse = await refresh();
            const { access_token } = refreshResponse;

            const currentUser = await getCurrentUser(access_token);

            setAccessToken(access_token);
            setUser(currentUser);
        } catch {
            try {
                console.log("Refresh failed, creating guest session");

                const guestResponse = await createGuest();
                console.log("Guest session created", guestResponse);

                const { access_token } = guestResponse;
    
                const guestUser = await getCurrentUser(access_token);
                console.log("Guest user", guestUser);

                setAccessToken(access_token);
                setUser(guestUser);
            } catch (error) {
                console.error("Guest session failed", error);
                setAccessToken(null);
                setUser(null);
            }
        } finally {
            setLoading(false);
        }
    }

    async function logout() {
        await logoutApi();
    
        setAccessToken(null);
        setUser(null);
    }

    // useEffect(() => {
    //     checkAuth();
    // }, []);
    useEffect(() => {
        if (authCheckStarted.current) {
            return;
        }

        authCheckStarted.current = true;
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