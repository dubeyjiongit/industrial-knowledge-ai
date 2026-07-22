import hashlib
from typing import List, Dict, Any

class TextChunker:
    @staticmethod
    def chunk_document(doc_id: str, filename: str, text: str, chunk_size: int = 400, overlap: int = 50) -> List[Dict[str, Any]]:
        words = text.split()
        if not words:
            return []

        chunks = []
        i = 0
        chunk_idx = 0

        while i < len(words):
            chunk_words = words[i:i + chunk_size]
            chunk_text = " ".join(chunk_words)
            chunk_hash = hashlib.md5(f"{doc_id}_{chunk_idx}_{chunk_text[:30]}".encode()).hexdigest()

            chunks.append({
                "id": chunk_hash,
                "doc_id": doc_id,
                "filename": filename,
                "chunk_index": chunk_idx,
                "content": chunk_text,
                "metadata": {
                    "word_count": len(chunk_words),
                    "start_word": i,
                    "end_word": i + len(chunk_words)
                }
            })

            chunk_idx += 1
            i += (chunk_size - overlap)

        return chunks
