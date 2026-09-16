const BASE_URL = "http://localhost:8000";

async function handleResponse(res) {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed with status ${res.status}`);
  }
  // 204 No Content has no body to parse
  if (res.status === 204) return null;
  return res.json();
}

export async function fetchProjects() {
  const res = await fetch(`${BASE_URL}/projects/`);
  return handleResponse(res);
}

export async function fetchProject(id) {
  const res = await fetch(`${BASE_URL}/projects/${id}`);
  return handleResponse(res);
}

export async function createProject(data) {
  const res = await fetch(`${BASE_URL}/projects/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}

export async function fetchProgress(projectId) {
  const res = await fetch(`${BASE_URL}/projects/${projectId}/progress`);
  return handleResponse(res);
}

export async function createMilestone(projectId, data) {
  const res = await fetch(`${BASE_URL}/projects/${projectId}/milestones`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}

export async function updateMilestone(milestoneId, data) {
  const res = await fetch(`${BASE_URL}/projects/milestones/${milestoneId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}
