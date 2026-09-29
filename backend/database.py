"""SQLite storage. One table, results stored as JSON text."""
import json
import sqlite3
from pathlib import Path

DB_PATH = Path("data/documents.db")


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS documents (
            document_id TEXT PRIMARY KEY,
            filename TEXT, original_path TEXT, image_path TEXT,
            status TEXT DEFAULT 'UPLOADED',
            result_json TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")


def next_id():
    with _conn() as c:
        n = c.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    return f"DOC-{n + 1:03d}"


def add_document(doc_id, filename, original_path, image_path):
    with _conn() as c:
        c.execute("INSERT INTO documents (document_id, filename, original_path, image_path) VALUES (?,?,?,?)",
                  (doc_id, filename, str(original_path), str(image_path)))


def save_result(doc_id, result: dict):
    with _conn() as c:
        c.execute("UPDATE documents SET status='ANALYZED', result_json=? WHERE document_id=?",
                  (json.dumps(result), doc_id))


def _row(r):
    d = dict(r)
    d["result"] = json.loads(d.pop("result_json")) if d.get("result_json") else None
    return d


def get_document(doc_id):
    with _conn() as c:
        r = c.execute("SELECT * FROM documents WHERE document_id=?", (doc_id,)).fetchone()
    return _row(r) if r else None


def list_documents():
    with _conn() as c:
        rows = c.execute("SELECT * FROM documents ORDER BY created_at, document_id").fetchall()
    return [_row(r) for r in rows]


def roll_numbers(exclude_id=None):
    """Roll numbers already seen in other analyzed documents (for duplicate check)."""
    rolls = []
    for d in list_documents():
        if d["document_id"] != exclude_id and d["result"]:
            rn = d["result"]["entities"].get("roll_number")
            if rn:
                rolls.append(rn)
    return rolls
