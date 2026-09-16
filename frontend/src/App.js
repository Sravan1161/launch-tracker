import React, { useState } from "react";
import ProjectList from "./components/ProjectList";
import ProjectDetail from "./components/ProjectDetail";
import "./App.css";

export default function App() {
  const [selectedProjectId, setSelectedProjectId] = useState(null);

  return (
    <div className="app">
      <header className="app-header">
        <h1>Launch Tracker</h1>
        <p className="tagline">From idea to launch, one milestone at a time.</p>
      </header>

      <main>
        {selectedProjectId ? (
          <ProjectDetail
            projectId={selectedProjectId}
            onBack={() => setSelectedProjectId(null)}
          />
        ) : (
          <ProjectList onSelectProject={setSelectedProjectId} />
        )}
      </main>
    </div>
  );
}
