import sqlite3
import os
import json
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_graph.db")

class KnowledgeGraphStore:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Documents table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    filename TEXT NOT NULL,
                    doc_type TEXT,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    chunk_count INTEGER DEFAULT 0
                )
            """)

            # Entities table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS entities (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    entity_type TEXT NOT NULL,
                    description TEXT
                )
            """)

            # Triples table (Subject - Predicate - Object)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS triples (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject TEXT NOT NULL,
                    predicate TEXT NOT NULL,
                    object TEXT NOT NULL,
                    source_doc TEXT,
                    FOREIGN KEY (source_doc) REFERENCES documents (id)
                )
            """)
            conn.commit()

    def add_document(self, doc_id: str, filename: str, doc_type: str, chunk_count: int):
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO documents (id, filename, doc_type, chunk_count)
                VALUES (?, ?, ?, ?)
            """, (doc_id, filename, doc_type, chunk_count))
            conn.commit()

    def add_entity(self, entity_id: str, name: str, entity_type: str, description: str = ""):
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO entities (id, name, entity_type, description)
                VALUES (?, ?, ?, ?)
            """, (entity_id, name, entity_type, description))
            conn.commit()

    def add_triple(self, subject: str, predicate: str, obj: str, source_doc: str):
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO triples (subject, predicate, object, source_doc)
                VALUES (?, ?, ?, ?)
            """, (subject, predicate, obj, source_doc))
            conn.commit()

    def get_entity_triples(self, entity_id: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT subject, predicate, object, source_doc FROM triples
                WHERE LOWER(subject) LIKE ? OR LOWER(object) LIKE ?
            """, (f"%{entity_id.lower()}%", f"%{entity_id.lower()}%"))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_all_entities(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM entities")
            return [dict(r) for r in cursor.fetchall()]

    def get_all_documents(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM documents ORDER BY uploaded_at DESC")
            return [dict(r) for r in cursor.fetchall()]

    def get_stats(self) -> Dict[str, int]:
        with self._get_connection() as conn:
            c = conn.cursor()
            doc_count = c.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
            entity_count = c.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
            triple_count = c.execute("SELECT COUNT(*) FROM triples").fetchone()[0]
            return {
                "total_documents": doc_count,
                "total_entities": entity_count,
                "total_triples": triple_count
            }

kg_store = KnowledgeGraphStore()
