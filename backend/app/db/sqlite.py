from pathlib import Path
import sqlite3

DB_PATH = Path("data/sentinel.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def ensure_db():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                organization TEXT,
                industry TEXT,
                evidence_type TEXT,
                review_objective TEXT,
                overall_rating TEXT,
                evidence_defensibility_score INTEGER,
                intake_coverage_score INTEGER,
                metadata_completeness_score INTEGER,
                total_findings INTEGER,
                payload_json TEXT NOT NULL,
                result_json TEXT NOT NULL,
                register_json TEXT NOT NULL
            )
        """)
        conn.commit()

