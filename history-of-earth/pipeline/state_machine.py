"""
Pipeline State Machine for History of Earth.
Manages episode lifecycle states according to the project state machine diagram:
idea -> researched -> fact_checked -> scripted -> [Gate A] -> storyboarded ->
art_directed -> rendered_frames -> narrated -> assembled -> compliance_checked ->
[Gate B] -> scheduled -> published -> analysed
"""

import os
import sqlite3
from typing import List, Dict, Optional, Any

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "state.db")
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db_schema.sql")

VALID_STATES = (
    "idea",
    "researched",
    "fact_checked",
    "scripted",
    "storyboarded",
    "art_directed",
    "rendered_frames",
    "narrated",
    "assembled",
    "compliance_checked",
    "scheduled",
    "published",
    "analysed",
)


def get_db_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Returns a SQLite connection with Row factory enabled."""
    target_path = db_path or os.environ.get("STATE_DB_PATH", DEFAULT_DB_PATH)
    conn = sqlite3.connect(target_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Optional[str] = None) -> None:
    """Initializes the database schema if not already present."""
    conn = get_db_connection(db_path)
    with conn:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
    conn.close()


def create_episode(
    episode_id: str,
    era: str,
    pillar: str,
    initial_state: str = "idea",
    db_path: Optional[str] = None
) -> Dict[str, Any]:
    """Creates a new episode entry in the state database."""
    init_db(db_path)
    if initial_state not in VALID_STATES:
        raise ValueError(f"Invalid initial state '{initial_state}'. Valid states: {list(VALID_STATES)}")

    conn = get_db_connection(db_path)
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO episodes (id, era, pillar, state)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                era = excluded.era,
                pillar = excluded.pillar,
                updated_at = CURRENT_TIMESTAMP
            """,
            (episode_id, era, pillar, initial_state),
        )
        cursor.execute("SELECT * FROM episodes WHERE id = ?", (episode_id,))
        row = cursor.fetchone()
    conn.close()
    return dict(row) if row else {}


def transition(episode_id: str, new_state: str, note: str = "", db_path: Optional[str] = None) -> None:
    """
    Transitions an episode to a new state with an optional note.
    Rejects any state not in VALID_STATES.
    """
    if new_state not in VALID_STATES:
        raise ValueError(
            f"Invalid state '{new_state}'. Valid states: {list(VALID_STATES)}"
        )

    init_db(db_path)
    conn = get_db_connection(db_path)
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM episodes WHERE id = ?", (episode_id,))
        existing = cursor.fetchone()
        if not existing:
            raise ValueError(f"Episode '{episode_id}' does not exist in state database.")

        # Determine how to append note (Gate A vs Gate B tracking)
        gate_a_notes = existing["gate_a_notes"] or ""
        gate_b_notes = existing["gate_b_notes"] or ""

        if note:
            formatted_note = f"[{new_state}] {note}"
            if new_state in ("idea", "researched", "fact_checked", "scripted") or "gate_a" in note.lower():
                gate_a_notes = f"{gate_a_notes}\n{formatted_note}".strip()
            else:
                gate_b_notes = f"{gate_b_notes}\n{formatted_note}".strip()

        cursor.execute(
            """
            UPDATE episodes
            SET state = ?,
                gate_a_notes = ?,
                gate_b_notes = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (new_state, gate_a_notes, gate_b_notes, episode_id),
        )
    conn.close()


def get_episodes_by_state(state: str, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieves all episodes in a given state.
    Rejects any state not in VALID_STATES.
    """
    if state not in VALID_STATES:
        raise ValueError(
            f"Invalid state '{state}'. Valid states: {list(VALID_STATES)}"
        )

    init_db(db_path)
    conn = get_db_connection(db_path)
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM episodes WHERE state = ? ORDER BY created_at ASC", (state,))
        rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
