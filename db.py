"""Database interaction module for SQLite (chat_logs.db).

Stores conversational interactions, user feedback (thumbs up/down),
retrieval confidence scores, and powers the Admin dashboard's unanswered
question analysis.
"""

import sqlite3
import os
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chat_logs.db")


def get_db_connection() -> sqlite3.Connection:
    """Create and configure a thread-safe connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables with appropriate indexes."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                category_filter TEXT,
                matched_faq_id INTEGER,
                score REAL NOT NULL,
                source TEXT NOT NULL,
                helpful INTEGER DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_logs_score ON chat_logs(score)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_logs_created ON chat_logs(created_at)")
        conn.commit()


def log_query(
    query: str,
    category_filter: Optional[str],
    matched_faq_id: Optional[int],
    score: float,
    source: str
) -> int:
    """Record an incoming student question and its retrieval outcome."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO chat_logs (query, category_filter, matched_faq_id, score, source, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (query, category_filter, matched_faq_id, round(score, 4), source, datetime.now(timezone.utc).isoformat())
        )
        conn.commit()
        return cursor.lastrowid


def update_feedback(log_id: int, helpful: bool) -> bool:
    """Update user satisfaction feedback (thumbs up = 1, thumbs down = 0)."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE chat_logs
            SET helpful = ?
            WHERE id = ?
            """,
            (1 if helpful else 0, log_id)
        )
        conn.commit()
        return cursor.rowcount > 0


def get_frequent_unanswered(threshold: float = 0.35, limit: int = 20) -> List[Dict[str, Any]]:
    """Aggregate questions where confidence fell below threshold or fallback occurred.

    Groups similar queries by normalized lowercase text to highlight gaps in college FAQs.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                LOWER(TRIM(query)) AS clean_query,
                COUNT(*) AS count,
                AVG(score) AS avg_score,
                MAX(created_at) AS last_seen
            FROM chat_logs
            WHERE score < ? OR source = 'fallback'
            GROUP BY clean_query
            ORDER BY count DESC, last_seen DESC
            LIMIT ?
            """,
            (threshold, limit)
        )
        rows = cursor.fetchall()
        return [
            {
                "query": row["clean_query"],
                "count": row["count"],
                "avg_confidence": round(row["avg_score"], 3),
                "last_seen": row["last_seen"]
            }
            for row in rows
        ]


def get_feedback_stats() -> Dict[str, Any]:
    """Retrieve aggregate thumbs up vs thumbs down metrics."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                COUNT(*) AS total_rated,
                SUM(CASE WHEN helpful = 1 THEN 1 ELSE 0 END) AS thumbs_up,
                SUM(CASE WHEN helpful = 0 THEN 1 ELSE 0 END) AS thumbs_down
            FROM chat_logs
            WHERE helpful IS NOT NULL
            """
        )
        row = cursor.fetchone()
        total = row["total_rated"] or 0
        up = row["thumbs_up"] or 0
        down = row["thumbs_down"] or 0
        rate = round((up / total * 100), 1) if total > 0 else 0.0
        return {
            "total_feedback": total,
            "thumbs_up": up,
            "thumbs_down": down,
            "satisfaction_rate_percent": rate
        }
