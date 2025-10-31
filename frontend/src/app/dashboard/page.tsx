'use client';

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { api, type InterviewSession, type InterviewTemplate } from "../../lib/api";
import { useAuth } from "../../context/AuthContext";

export default function DashboardPage() {
  const router = useRouter();
  const { user, token, loading, logout } = useAuth();
  const [templates, setTemplates] = useState<InterviewTemplate[]>([]);
  const [sessions, setSessions] = useState<InterviewSession[]>([]);
  const [formState, setFormState] = useState({
    candidate_name: "",
    candidate_email: "",
    role: "Full Stack Engineer",
    template_id: ""
  });
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLoadingSessions, setIsLoadingSessions] = useState(false);

  useEffect(() => {
    if (!loading && !token) {
      router.replace("/login");
    }
  }, [loading, token, router]);

  useEffect(() => {
    if (!token) return;
    let isActive = true;

    const bootstrap = async () => {
      try {
        const [fetchedTemplates, fetchedSessions] = await Promise.all([
          api.listTemplates(token),
          api.listSessions(token)
        ]);
        if (!isActive) return;
        setTemplates(fetchedTemplates);
        setSessions(fetchedSessions.items);
        if (!formState.template_id && fetchedTemplates.length > 0) {
          setFormState((prev) => ({ ...prev, template_id: fetchedTemplates[0].id }));
        }
      } catch (err) {
        console.error(err);
        setError(err instanceof Error ? err.message : "Unable to load data");
      }
    };

    bootstrap();
    return () => {
      isActive = false;
    };
  }, [token]);

  const handleCreateSession = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!token) return;
    setIsSubmitting(true);
    setError(null);
    try {
      const payload = {
        candidate_name: formState.candidate_name,
        candidate_email: formState.candidate_email || undefined,
        role: formState.role,
        template_id: formState.template_id
      };
      const created = await api.createSession(token, payload);
      setSessions((prev) => [created, ...prev]);
      setFormState((prev) => ({ ...prev, candidate_name: "", candidate_email: "" }));
      router.push(`/interviews/${created.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to create session");
    } finally {
      setIsSubmitting(false);
    }
  };

  const refreshSessions = async () => {
    if (!token) return;
    setIsLoadingSessions(true);
    try {
      const response = await api.listSessions(token);
      setSessions(response.items);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to refresh sessions");
    } finally {
      setIsLoadingSessions(false);
    }
  };

  const templateOptions = useMemo(() => {
    return templates.map((template) => (
      <option key={template.id} value={template.id}>
        {template.title}
      </option>
    ));
  }, [templates]);

  if (!user && loading) {
    return <p className="muted">Preparing your interview HQ…</p>;
  }

  return (
    <div className="grid" style={{ gap: "2rem" }}>
      <section className="card">
        <div className="flex-between" style={{ marginBottom: "1.5rem" }}>
          <div>
            <h2 style={{ fontSize: "1.5rem" }}>Start a new interview</h2>
            <p className="muted">Launch the Soal Labs punchy framework in a few clicks.</p>
          </div>
          <button className="button" style={{ background: "transparent", color: "var(--text-secondary)" }} onClick={logout}>
            Log out
          </button>
        </div>
        <form className="grid" style={{ gap: "1rem" }} onSubmit={handleCreateSession}>
          <label className="stack" style={{ gap: "0.35rem" }}>
            <span className="muted">Candidate name</span>
            <input
              className="input"
              value={formState.candidate_name}
              onChange={(event) => setFormState((prev) => ({ ...prev, candidate_name: event.target.value }))}
              placeholder="Candidate name"
              required
            />
          </label>
          <label className="stack" style={{ gap: "0.35rem" }}>
            <span className="muted">Candidate email (optional)</span>
            <input
              className="input"
              type="email"
              value={formState.candidate_email}
              onChange={(event) => setFormState((prev) => ({ ...prev, candidate_email: event.target.value }))}
              placeholder="candidate@example.com"
            />
          </label>
          <label className="stack" style={{ gap: "0.35rem" }}>
            <span className="muted">Role / track</span>
            <input
              className="input"
              value={formState.role}
              onChange={(event) => setFormState((prev) => ({ ...prev, role: event.target.value }))}
              placeholder="Full Stack Engineer"
              required
            />
          </label>
          <label className="stack" style={{ gap: "0.35rem" }}>
            <span className="muted">Interview framework</span>
            <select
              className="select"
              value={formState.template_id}
              onChange={(event) => setFormState((prev) => ({ ...prev, template_id: event.target.value }))}
            >
              {templateOptions}
            </select>
          </label>
          {error ? <p style={{ color: "#ff7b7b" }}>{error}</p> : null}
          <button className="button" type="submit" disabled={isSubmitting || !formState.template_id}>
            {isSubmitting ? "Creating" : "Create interview"}
          </button>
        </form>
      </section>

      <section className="card">
        <div className="flex-between" style={{ marginBottom: "1rem" }}>
          <div>
            <h2 style={{ fontSize: "1.25rem" }}>Active interviews</h2>
            <p className="muted">All sessions you own. Admins see everything.</p>
          </div>
          <button className="button" style={{ background: "transparent", color: "var(--text-secondary)" }} onClick={refreshSessions} disabled={isLoadingSessions}>
            {isLoadingSessions ? "Refreshing…" : "Refresh"}
          </button>
        </div>
        <table className="table">
          <thead>
            <tr>
              <th>Candidate</th>
              <th>Role</th>
              <th>Status</th>
              <th>Updated</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {sessions.length === 0 ? (
              <tr>
                <td colSpan={5} className="muted">
                  No interviews yet. Spin up the punchy flow above.
                </td>
              </tr>
            ) : (
              sessions.map((session) => (
                <tr key={session.id}>
                  <td>{session.candidate_name}</td>
                  <td>{session.role}</td>
                  <td>
                    <span className="badge">{session.status}</span>
                  </td>
                  <td>{new Date(session.updated_at).toLocaleDateString()}</td>
                  <td>
                    <Link className="button" style={{ padding: "0.35rem 0.85rem" }} href={`/interviews/${session.id}`}>
                      Open
                    </Link>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>

      <section className="card">
        <h2 style={{ fontSize: "1.25rem", marginBottom: "0.75rem" }}>Framework snapshot</h2>
        <div className="stack">
          {templates.map((template) => (
            <article key={template.id} className="stack" style={{ gap: "0.5rem" }}>
              <header className="flex-between">
                <div>
                  <h3 style={{ fontSize: "1.1rem" }}>{template.title}</h3>
                  <p className="muted">{template.description}</p>
                </div>
                <div className="flex" style={{ flexWrap: "wrap" }}>
                  {template.tags.map((tag) => (
                    <span className="badge" key={tag}>
                      {tag}
                    </span>
                  ))}
                </div>
              </header>
              <div className="stack" style={{ gap: "0.35rem" }}>
                {template.phases.map((phase) => (
                  <div key={String(phase["id"])} style={{ borderLeft: "2px solid var(--border)", paddingLeft: "0.75rem" }}>
                    <strong>{phase["title"] as string}</strong>
                    {phase["focus"] ? (
                      <p className="muted">Focus: {(phase["focus"] as string[]).join(", ")}</p>
                    ) : null}
                  </div>
                ))}
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
