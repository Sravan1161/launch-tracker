import React, { useEffect, useState } from "react";
import {
  fetchProject,
  fetchProgress,
  createMilestone,
  updateMilestone,
} from "../api/projects";

const STAGES = ["idea", "mvp", "beta", "launch"];

export default function ProjectDetail({ projectId, onBack }) {
  const [project, setProject] = useState(null);
  const [progress, setProgress] = useState(null);
  const [title, setTitle] = useState("");
  const [stage, setStage] = useState("idea");
  const [error, setError] = useState(null);

  const loadData = async () => {
    try {
      const [projectData, progressData] = await Promise.all([
        fetchProject(projectId),
        fetchProgress(projectId),
      ]);
      setProject(projectData);
      setProgress(progressData);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [projectId]);

  const handleAddMilestone = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    try {
      await createMilestone(projectId, { title, stage, status: "pending" });
      setTitle("");
      loadData();
    } catch (err) {
      setError(err.message);
    }
  };

  const toggleMilestone = async (milestone) => {
    const nextStatus = milestone.status === "done" ? "pending" : "done";
    try {
      await updateMilestone(milestone.id, { status: nextStatus });
      loadData();
    } catch (err) {
      setError(err.message);
    }
  };

  if (error) return <p className="error">Error: {error}</p>;
  if (!project) return <p>Loading…</p>;

  return (
    <div className="project-detail">
      <button onClick={onBack} className="back-button">← Back</button>
      <h2>{project.name}</h2>
      <span className={`stage-badge stage-${project.stage}`}>{project.stage}</span>

      {progress && (
        <div className="progress-section">
          <div className="progress-bar-track">
            <div
              className="progress-bar-fill"
              style={{ width: `${progress.percent_complete}%` }}
            />
          </div>
          <p>
            {progress.completed_milestones} / {progress.total_milestones} milestones
            complete ({progress.percent_complete}%)
          </p>
        </div>
      )}

      <form onSubmit={handleAddMilestone} className="new-milestone-form">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="New milestone"
        />
        <select value={stage} onChange={(e) => setStage(e.target.value)}>
          {STAGES.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
        <button type="submit">Add Milestone</button>
      </form>

      <ul className="milestone-list">
        {project.milestones.map((m) => (
          <li key={m.id} className={m.status === "done" ? "done" : ""}>
            <input
              type="checkbox"
              checked={m.status === "done"}
              onChange={() => toggleMilestone(m)}
            />
            <span className="milestone-title">{m.title}</span>
            <span className={`stage-badge stage-${m.stage}`}>{m.stage}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
