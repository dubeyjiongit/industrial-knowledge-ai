import sqlite3
import os
import json
import math
import numpy as np
from typing import List, Dict, Any, Optional

VECTOR_DB_PATH = os.path.join(os.path.dirname(__file__), "vector_store.db")

class VectorStore:
    def __init__(self, db_path: str = VECTOR_DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                    id TEXT PRIMARY KEY,
                    doc_id TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    chunk_index INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    metadata_json TEXT
                )
            """)
            conn.commit()

    def _tokenize(self, text: str) -> List[str]:
        # Simple clean regex tokenizer
        import re
        words = re.findall(r'\w+', text.lower())
        return [w for w in words if len(w) > 2]

    def _get_tf_vector(self, text: str, vocabulary: List[str]) -> np.ndarray:
        tokens = self._tokenize(text)
        total = max(len(tokens), 1)
        counts = {}
        for t in tokens:
            counts[t] = counts.get(t, 0) + 1
        return np.array([counts.get(word, 0) / total for word in vocabulary], dtype=np.float32)

    def add_chunks(self, chunks: List[Dict[str, Any]]):
        """
        chunks is a list of dicts:
        [{ 'id': str, 'doc_id': str, 'filename': str, 'chunk_index': int, 'content': str, 'metadata': dict }]
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for c in chunks:
                cursor.execute("""
                    INSERT OR REPLACE INTO chunks (id, doc_id, filename, chunk_index, content, metadata_json)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    c['id'],
                    c['doc_id'],
                    c['filename'],
                    c['chunk_index'],
                    c['content'],
                    json.dumps(c.get('metadata', {}))
                ))
            conn.commit()

    def query(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM chunks")
            rows = cursor.fetchall()

        if not rows:
            return []

        all_chunks = [dict(r) for r in rows]

        # Build vocabulary across query and stored chunks
        query_tokens = set(self._tokenize(query_text))
        
        # Calculate TF-IDF / keyword similarity score for each chunk
        results = []
        for chunk in all_chunks:
            content = chunk['content']
            content_lower = content.lower()
            
            # Match score based on keyword overlaps and exact term matches
            score = 0.0
            for token in query_tokens:
                if token in content_lower:
                    # Count occurrences
                    cnt = content_lower.count(token)
                    score += (1.0 + math.log(cnt))

            # Extra weight if equipment codes match directly (e.g. C-102, PRV-88)
            import re
            equipment_codes = re.findall(r'[a-zA-Z]+-\d+', query_text.upper())
            for eq in equipment_codes:
                if eq in content.upper():
                    score += 5.0

            results.append({
                "chunk": chunk,
                "score": score
            })

        # Sort descending by score
        results.sort(key=lambda x: x['score'], reverse=True)
        top_results = results[:n_results]

        output = []
        for item in top_results:
            ch = item['chunk']
            metadata = json.loads(ch['metadata_json']) if ch['metadata_json'] else {}
            output.append({
                "id": ch['id'],
                "doc_id": ch['doc_id'],
                "filename": ch['filename'],
                "chunk_index": ch['chunk_index'],
                "content": ch['content'],
                "metadata": metadata,
                "score": round(item['score'], 4)
            })

        return output

vector_store = VectorStore()
