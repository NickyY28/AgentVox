"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { api } from "../lib/api";
import { useRouter } from "next/router";

export interface User {
    id: number;
    email: string;
    full_name: string | null;
    is_active: boolean;
}

interface AuthContextType {
    user: User | null;
    isLoading: boolean;
    login: (email: string, password: string) => Promise<void>;
    signup: (email: string, password: string, fullName: string) => Promise<void>;
    logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);
export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const router = useRouter();
    useEffect(() => {
        checkUser();
    }, []);
    const checkUser = async () => {
        try {
            const response = await api.get("/auth/me");
            setUser(response.data);
        } catch (error) {
            setUser(null);
        } finally {
            setIsLoading(false);
        }
    };
    const login = async (email: string, password: string) => {
        await api.post("/auth/login", { email, password });
        await checkUser();
        router.push("/");
    };
    const signup = async (email: string, password: string, fullName: string) => {
        await api.post("/auth/signup", { email, password, full_name: fullName });
        await login(email, password);
    };
    const logout = async () => {
        await api.post("/auth/logout");
        setUser(null);
        router.push("/login");
    };
    return (
        <AuthContext.Provider value={{ user, isLoading, login, signup, logout }}>
            {children}
        </AuthContext.Provider>
    );
}
export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
}
