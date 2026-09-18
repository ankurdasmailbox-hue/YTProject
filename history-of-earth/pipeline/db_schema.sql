-- Schema for History of Earth Pipeline State Database
CREATE TABLE IF NOT EXISTS episodes (
    id TEXT PRIMARY KEY,
    era TEXT NOT NULL,
    pillar TEXT NOT NULL,
    state TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    script_path TEXT,
    storyboard_path TEXT,
    video_path TEXT,
    metadata_json TEXT,
    gate_a_notes TEXT,
    gate_b_notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_episodes_state ON episodes(state);
CREATE INDEX IF NOT EXISTS idx_episodes_era_pillar ON episodes(era, pillar);
