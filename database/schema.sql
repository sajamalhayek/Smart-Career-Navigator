CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    resume_text TEXT,
    skills_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS gap_analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER,
    target_job TEXT,
    match_percentage INTEGER,
    missing_skills_json TEXT,
    roadmap_json TEXT,
    FOREIGN KEY(candidate_id) REFERENCES candidates(id)
);