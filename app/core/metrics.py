import sqlite3
import time
from app.core.config import settings

def init_db():
    """
    Initializes the SQLite database for evaluation metrics.
    """
    conn = sqlite3.connect(settings.metrics_db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            session_id TEXT,
            query TEXT,
            response TEXT,
            agent_used TEXT,
            confidence REAL,
            latency_ms REAL
        )
    ''')
    conn.commit()
    conn.close()

def log_interaction(session_id: str, query: str, response: str, agent_used: str, confidence: float, latency_ms: float):
    """
    Logs a single interaction to the database.
    """
    conn = sqlite3.connect(settings.metrics_db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO interactions (timestamp, session_id, query, response, agent_used, confidence, latency_ms)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (time.time(), session_id, query, response, agent_used, confidence, latency_ms))
    conn.commit()
    conn.close()

# Initialize DB on load
init_db()
