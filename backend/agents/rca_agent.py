import json
import re
from typing import Dict, Any, List
from storage.vector_store import vector_store
from storage.knowledge_graph import kg_store
from llm.llm_provider import llm_provider

class RcaAgent:
    @staticmethod
    def analyze_equipment(equipment_id: str) -> Dict[str, Any]:
        eq_clean = equipment_id.strip().upper()

        # 1. Retrieve all chunks mentioning equipment_id
        chunks = vector_store.query(eq_clean, n_results=10)

        # 2. Retrieve all KG triples
        triples = kg_store.get_entity_triples(eq_clean)

        # Build chronological timeline from retrieved text
        timeline_events = []
        for c in chunks:
            content = c['content']
            # Find date strings like 14-Jul-2023 or 12-Mar-2023
            dates = re.findall(r'\b\d{1,2}-[A-Za-z]{3}-\d{4}\b', content)
            date_str = dates[0] if dates else "Unknown Date"

            # Identify issue / event summary
            issue_match = re.search(r'(?:Issue Reported|FINDINGS|Action Taken):\s*([^.\n]+)', content, re.IGNORECASE)
            summary = issue_match.group(1).strip() if issue_match else content[:120] + "..."

            timeline_events.append({
                "date": date_str,
                "document": c['filename'],
                "summary": summary,
                "full_text": content
            })

        # Sort timeline if dates found
        timeline_events.sort(key=lambda x: x['date'])

        # Prepare context for RCA LLM Reasoning
        context_str = f"EQUIPMENT UNDER ANALYSIS: {eq_clean}\n\n"
        context_str += "--- CHRONOLOGICAL MAINTENANCE & INSPECTION RECORDS ---\n"
        for ev in timeline_events:
            context_str += f"Date: {ev['date']} | Doc: {ev['document']}\nEvent: {ev['summary']}\nDetails:\n{ev['full_text']}\n"
            context_str += "-" * 50 + "\n"

        if triples:
            context_str += "\n--- KNOWLEDGE GRAPH RELATIONAL TRIPLES ---\n"
            for tr in triples:
                context_str += f"({tr['subject']}) --[{tr['predicate']}]--> ({tr['object']}) [Ref: {tr['source_doc']}]\n"

        system_prompt = (
            "You are a Principal Reliability & Root Cause Analysis (RCA) Engineer for an Oil Refinery. "
            f"Analyze the operational failure history for Equipment {eq_clean}. "
            "You MUST structure your analysis cleanly into:\n"
            "1. **Operational History & Failure Pattern**: Identify recurring patterns (e.g. monsoon moisture, seal wear, valve failure).\n"
            "2. **Identified Root Cause**: The underlying engineering/operational failure mode.\n"
            "3. **Violated SOP / Compliance Risk**: Mention any procedures or standards (e.g. OISD-116, SOP-04).\n"
            "4. **Predictive Maintenance & Preventative Recommendations**: Bulleted, actionable steps to prevent future downtime."
        )

        user_prompt = f"Records Context:\n{context_str}\n\nPerform a comprehensive RCA analysis for Equipment {eq_clean}."

        rca_report = llm_provider.generate_text(prompt=user_prompt, system_prompt=system_prompt)

        return {
            "equipment_id": eq_clean,
            "timeline": timeline_events,
            "triples": triples,
            "rca_report": rca_report,
            "record_count": len(chunks)
        }
