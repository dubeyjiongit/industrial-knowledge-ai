import json
import re
from typing import Dict, Any, List
from rag.retriever import HybridRetriever
from llm.llm_provider import llm_provider

class RAGQueryEngine:
    @staticmethod
    def answer_question(question: str) -> Dict[str, Any]:
        clean_q = question.strip()
        lower_q = clean_q.lower()

        # Detect conversational greetings / small talk (catches hi, hii, hiiii, hello, helloo, hey, heyy, etc.)
        greeting_pattern = r'\b(h[ia]+|he+l+o+|he+y+|namaste|greetings|good\s+(morning|afternoon|evening)|what\'?s\s+up)\b'
        is_greeting = bool(re.search(greeting_pattern, lower_q))
        is_intro = any(phrase in lower_q for phrase in ["my name is", "i am", "i'm", "who are you", "what can you do", "help me"])

        if (is_greeting or is_intro) and len(clean_q.split()) < 10 and not any(code in clean_q.upper() for code in ["C-102", "PRV-88", "WO-", "IR-", "SOP-", "SP-"]):
            answer_text = (
                "Hello! 👋 Welcome to the **Unified Asset & Operations Brain**.\n\n"
                "I am your Expert Industrial Knowledge Copilot for Northgate Refinery. "
                "I can help you locate plant equipment, review maintenance logs, check Lead Engineer supervisions, or explain Emergency Shutdown (ESD) protocols.\n\n"
                "How can I assist you today?"
            )
            return {
                "question": question,
                "answer": answer_text,
                "citations": [],
                "confidence": 1.0,
                "retrieved_chunks": [],
                "retrieved_triples": []
            }

        # 1. Retrieve hybrid context for technical queries
        retrieved = HybridRetriever.retrieve(clean_q, top_k=4)
        chunks = retrieved['chunks']
        triples = retrieved['triples']

        # Format context for LLM
        context_str = "--- RETRIEVED INDUSTRIAL DOCUMENTS & RECORDS ---\n"
        citations = []

        for i, c in enumerate(chunks, 1):
            fn = c['filename']
            doc_id = c['doc_id']
            if fn not in [cit['filename'] for cit in citations]:
                citations.append({
                    "doc_id": doc_id,
                    "filename": fn,
                    "score": c['score']
                })
            context_str += f"\n[SOURCE {i}: {fn}]\n{c['content']}\n"

        if triples:
            context_str += "\n--- KNOWLEDGE GRAPH RELATIONAL TRIPLES ---\n"
            for tr in triples[:10]:
                context_str += f"({tr['subject']}) --[{tr['predicate']}]--> ({tr['object']}) [Source: {tr['source_doc']}]\n"

        system_prompt = (
            "You are the Expert Knowledge Copilot for Northgate Refinery. "
            "Your job is to answer operational, engineering, and maintenance questions concisely and accurately. "
            "Always reference exact Equipment IDs (e.g. C-102, PRV-88), dates, and source documents when answering."
        )

        user_prompt = f"Context:\n{context_str}\n\nQuestion: {clean_q}\n\nPlease provide a clear, factual answer based strictly on the context above."

        raw_answer = llm_provider.generate_text(prompt=user_prompt, system_prompt=system_prompt)

        confidence = 0.95 if chunks and chunks[0]['score'] > 2.0 else (0.85 if chunks else 0.70)

        return {
            "question": question,
            "answer": raw_answer,
            "citations": citations,
            "confidence": round(confidence, 2),
            "retrieved_chunks": chunks,
            "retrieved_triples": triples
        }
