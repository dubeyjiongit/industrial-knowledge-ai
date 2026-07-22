import re
from typing import List, Dict, Any
from storage.vector_store import vector_store
from storage.knowledge_graph import kg_store

class HybridRetriever:
    @staticmethod
    def retrieve(query_text: str, top_k: int = 4) -> Dict[str, Any]:
        # 1. Semantic Vector Search
        chunks = vector_store.query(query_text, n_results=top_k)

        # 2. Knowledge Graph Triples Search
        # Extract potential equipment IDs or keywords
        keywords = re.findall(r'\b[A-Z0-9-]{3,10}\b', query_text.upper())
        triples = []
        matched_entities = []

        for kw in keywords:
            t = kg_store.get_entity_triples(kw)
            if t:
                triples.extend(t)
                matched_entities.append(kw)

        # Remove duplicate triples
        unique_triples = []
        seen = set()
        for tr in triples:
            key = (tr['subject'], tr['predicate'], tr['object'])
            if key not in seen:
                seen.add(key)
                unique_triples.append(tr)

        return {
            "chunks": chunks,
            "triples": unique_triples,
            "matched_entities": list(set(matched_entities))
        }
