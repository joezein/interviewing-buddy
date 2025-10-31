'use client';

import { useEffect, useMemo, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { api, type InterviewSession, type InterviewStep, type InterviewTemplate } from "../../../lib/api";
import { useAuth } from "../../../context/AuthContext";

interface StepDraft {
  notes: string;
  score: string;
  is_completed: boolean;
}

export default function InterviewDetailPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const { token, loading } = useAuth();

  const [sessionData, setSessionData] = useState<InterviewSession | null>(null);
  const [template, setTemplate] = useState<InterviewTemplate | null>(null);
  const [drafts, setDrafts] = useState<Record<string, StepDraft>>({});
  const [sessionNotes, setSessionNotes] = useState("");
  const [sessionScore, setSessionScore] = useState("");
  const [savingStep, setSavingStep] = useState<string | null>(null);
  const [savingSession, setSavingSession] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sessionId = params?.id;

  useEffect(() => {
    if (!loading && !token) {
      router.replace("/login");
    }
  }, [loading, token, router]);

  useEffect(() => {
    if (!token || !sessionId) return;

    const load = async () => {
      try {
        const [sessionResponse, templates] = await Promise.all([
          api.getSession(token, sessionId),
          api.listTemplates(token)
        ]);
        setSessionData(sessionResponse);
        setSessionNotes(sessionResponse.notes_summary ?? "");
        setSessionScore(sessionResponse.overall_score?.toString() ?? "");
        const templateMatch = templates.find((item) => item.id === sessionResponse.template_id);
        setTemplate(templateMatch ?? null);
        const initialDrafts: Record<string, StepDraft> = {};
        for (const step of sessionResponse.steps ?? []) {
          initialDrafts[step.id] = {
            notes: step.notes ?? "",
            score: step.score?.toString() ?? "",
            is_completed: step.is_completed
          };
        }
        setDrafts(initialDrafts);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unable to load interview");
      }
    };

    load();
  }, [token, sessionId]);

  const linkedTemplateSteps = useMemo(() => {
    if (!template || !sessionData?.steps) return [];
    const templateStepMap = Object.fromEntries((template.steps as any[])?.map((step) => [step.id, step]) ?? []);
    return sessionData.steps
      .slice()
      .sort((a, b) => a.order - b.order)
      .map((step) => ({
        step,
        templateDefinition: templateStepMap[step.template_step_id] ?? null
      }));
  }, [template, sessionData]);

  const handleDraftChange = (stepId: string, patch: Partial<StepDraft>) => {
    setDrafts((prev) => ({
      ...prev,
      [stepId]: {
        ...(prev[stepId] ?? { notes: "", score: "", is_completed: false }),
        ...patch
      }
    }));
  };

  const saveStep = async (step: InterviewStep) => {
    if (!token || !sessionId) return;
    const draft = drafts[step.id];
    if (!draft) return;
    setSavingStep(step.id);
    setError(null);
    try {
      const payload = {
        notes: draft.notes,
        score: draft.score ? Number(draft.score) : undefined,
        is_completed: draft.is_completed
      };
      const updated = await api.updateStep(token, sessionId, step.id, payload);
      setSessionData((prev) => {
        if (!prev || !prev.steps) return prev;
        return {
          ...prev,
          steps: prev.steps.map((item) => (item.id === updated.id ? updated : item))
        };
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to save step");
    } finally {
      setSavingStep(null);
    }
  };

  const saveSession = async () => {
    if (!token || !sessionId) return;
    setSavingSession(true);
    setError(null);
    try {
      const payload = {
        notes_summary: sessionNotes || undefined,
        overall_score: sessionScore ? Number(sessionScore) : undefined
      };
      const updated = await api.updateSession(token, sessionId, payload);
      setSessionData(updated);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to update interview summary");
    } finally {
      setSavingSession(false);
    }
  };

  if (!sessionData) {
    return <p className="muted">Loading interview detail…</p>;
  }

  return (
    <div className="stack" style={{ gap: "2rem" }}>
      <header className="card stack" style={{ gap: "0.75rem" }}>
        <div className="flex-between">
          <div>
            <h2 style={{ fontSize: "1.75rem" }}>{sessionData.candidate_name}</h2>
            <p className="muted">{sessionData.role}</p>
          </div>
          <span className="badge">{sessionData.status}</span>
        </div>
        <div className="stack" style={{ gap: "0.5rem" }}>
          <label className="stack" style={{ gap: "0.35rem" }}>
            <span className="muted">Overall recommendation notes</span>
            <textarea
              className="textarea"
              rows={5}
              value={sessionNotes}
              onChange={(event) => setSessionNotes(event.target.value)}
              placeholder="Summarize the candidate’s arc, risks, and punchline."
            />
          </label>
          <label className="stack" style={{ gap: "0.35rem", maxWidth: 200 }}>
            <span className="muted">Overall score (0-5)</span>
            <input
              className="input"
              type="number"
              min={0}
              max={5}
              step={0.1}
              value={sessionScore}
              onChange={(event) => setSessionScore(event.target.value)}
              placeholder="4.2"
            />
          </label>
        </div>
        <button className="button" onClick={saveSession} disabled={savingSession}>
          {savingSession ? "Saving…" : "Save summary"}
        </button>
        {error ? <p style={{ color: "#ff7b7b" }}>{error}</p> : null}
      </header>

      <div className="stack" style={{ gap: "1.5rem" }}>
        {linkedTemplateSteps.map(({ step, templateDefinition }) => {
          const draft = drafts[step.id] ?? { notes: "", score: "", is_completed: false };
          const saving = savingStep === step.id;
          return (
            <article key={step.id} className="card stack" style={{ gap: "1rem" }}>
              <header className="flex-between">
                <div>
                  <h3 style={{ fontSize: "1.3rem" }}>{step.title}</h3>
                  {templateDefinition?.summary ? (
                    <p className="muted">{String(templateDefinition.summary)}</p>
                  ) : null}
                </div>
                <div className="flex" style={{ alignItems: "center" }}>
                  <label className="flex" style={{ gap: "0.5rem" }}>
                    <input
                      type="checkbox"
                      checked={draft.is_completed}
                      onChange={(event) => handleDraftChange(step.id, { is_completed: event.target.checked })}
                    />
                    <span className="muted">Mark complete</span>
                  </label>
                </div>
              </header>
              {templateDefinition?.prompts ? (
                <div className="stack" style={{ gap: "0.5rem" }}>
                  <strong>Guidance</strong>
                  <GuidanceDisplay prompts={templateDefinition.prompts as Record<string, unknown>} />
                </div>
              ) : null}
              {templateDefinition?.scoring_guidance ? (
                <div className="stack" style={{ gap: "0.35rem" }}>
                  <strong>Score cues</strong>
                  <GuidanceDisplay prompts={templateDefinition.scoring_guidance as Record<string, unknown>} />
                </div>
              ) : null}
              <label className="stack" style={{ gap: "0.35rem" }}>
                <span className="muted">Notes</span>
                <textarea
                  className="textarea"
                  rows={6}
                  value={draft.notes}
                  onChange={(event) => handleDraftChange(step.id, { notes: event.target.value })}
                  placeholder="Capture verbatims, tone shifts, and surprises."
                />
              </label>
              <label className="stack" style={{ gap: "0.35rem", maxWidth: 180 }}>
                <span className="muted">Score (0-5)</span>
                <input
                  className="input"
                  type="number"
                  min={0}
                  max={5}
                  step={0.1}
                  value={draft.score}
                  onChange={(event) => handleDraftChange(step.id, { score: event.target.value })}
                  placeholder="4.0"
                />
              </label>
              <button className="button" onClick={() => saveStep(step)} disabled={saving}>
                {saving ? "Saving" : "Save step"}
              </button>
            </article>
          );
        })}
      </div>
    </div>
  );
}

function GuidanceDisplay({ prompts }: { prompts: Record<string, unknown> }) {
  return (
    <div className="stack" style={{ gap: "0.35rem" }}>
      {Object.entries(prompts).map(([key, value]) => {
        if (typeof value === "string") {
          return (
            <div key={key}>
              <span className="muted" style={{ textTransform: "capitalize" }}>
                {key.replace(/_/g, " ")}
              </span>
              <p>{value}</p>
            </div>
          );
        }
        if (Array.isArray(value)) {
          return (
            <div key={key} className="stack" style={{ gap: "0.25rem" }}>
              <span className="muted" style={{ textTransform: "capitalize" }}>
                {key.replace(/_/g, " ")}
              </span>
              <ul style={{ paddingLeft: "1rem", listStyle: "disc" }}>
                {value.map((item) => (
                  <li key={String(item)}>{String(item)}</li>
                ))}
              </ul>
            </div>
          );
        }
        if (value && typeof value === "object") {
          return (
            <div key={key} className="stack" style={{ gap: "0.25rem" }}>
              <span className="muted" style={{ textTransform: "capitalize" }}>
                {key.replace(/_/g, " ")}
              </span>
              <div className="stack" style={{ gap: "0.15rem" }}>
                {Object.entries(value as Record<string, unknown>).map(([innerKey, innerValue]) => (
                  <div key={innerKey} className="flex-between">
                    <span>{innerKey}</span>
                    <span className="muted">{String(innerValue)}</span>
                  </div>
                ))}
              </div>
            </div>
          );
        }
        return null;
      })}
    </div>
  );
}
