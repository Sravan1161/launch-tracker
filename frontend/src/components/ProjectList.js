import React, { useEffect, useState } from "react";
import { fetchProjects, createProject } from "../api/projects";

export default function ProjectList({ onSelectProject }) {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newName, setNewName] = useState("");

  const loadProjects = async () => {
    try {
      setLoading(true);
      const data = await fetchProjects();
      setProjects(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!newName.trim()) return;
    try {
      await createProject({ name: newName, stage: "idea" });
      setNewName("");
      loadProjects();
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <p>Loading projects…</p>;
  if (error) return <p className="error">Error: {error}</p>;

  return (
    <div className="project-list">
      <h2>Projects</h2>

      <form onSubmit={handleCreate} className="new-project-form">
        <input
          type="text"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          placeholder="New project name"
        />
        <button type="submit">Add Project</button>
      </form>

      {projects.length === 0 ? (
        <p>No projects yet — add one above.</p>
      ) : (
        <ul>
          {projects.map((p) => (
            <li key={p.id} onClick={() => onSelectProject(p.id)} className="project-item">
              <span className="project-name">{p.name}</span>
              <span className={`stage-badge stage-${p.stage}`}>{p.stage}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
