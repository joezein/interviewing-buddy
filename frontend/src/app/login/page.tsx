'use client';

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "../../context/AuthContext";

export default function LoginPage() {
  const router = useRouter();
  const { login, user, loading } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!loading && user) {
      router.replace("/dashboard");
    }
  }, [user, loading, router]);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await login(email, password);
      router.replace("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to login");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="card" style={{ maxWidth: 420, margin: "4rem auto" }}>
      <form className="stack" onSubmit={handleSubmit}>
        <div>
          <h2 style={{ fontSize: "1.5rem", marginBottom: "0.5rem" }}>Welcome back</h2>
          <p className="muted">Internal interview workspace. Use your company credentials.</p>
        </div>
        <label className="stack" style={{ gap: "0.35rem" }}>
          <span className="muted">Email</span>
          <input
            className="input"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="you@soal.labs"
            required
          />
        </label>
        <label className="stack" style={{ gap: "0.35rem" }}>
          <span className="muted">Password</span>
          <input
            className="input"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="••••••••"
            required
          />
        </label>
        {error ? (
          <p style={{ color: "#ff7b7b", fontSize: "0.85rem" }}>{error}</p>
        ) : null}
        <button className="button" type="submit" disabled={submitting}>
          {submitting ? "Signing in…" : "Sign in"}
        </button>
      </form>
    </div>
  );
}
