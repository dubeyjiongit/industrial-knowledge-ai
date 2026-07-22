import re
import json
from typing import Dict, Any, List
from storage.knowledge_graph import kg_store

class EntityExtractor:
    @staticmethod
    def process_and_store(doc_id: str, filename: str, text: str):
        # 1. Regex & Pattern Extraction for key equipment and document entities
        equipment_matches = set(re.findall(r'\b[A-Z]{1,3}-\d{2,4}[A-Z]?\b', text))
        wo_matches = set(re.findall(r'\bWO-\d{4}-\d{3,4}\b', text))
        ir_matches = set(re.findall(r'\bIR-\d{4}-\d{3,4}\b', text))
        sp_matches = set(re.findall(r'\bSP-\d{2,3}\b', text))
        sop_matches = set(re.findall(r'\bSOP-[A-Z0-9-]+\b', text))

        # Add Equipment Entities
        for eq in equipment_matches:
            kg_store.add_entity(
                entity_id=eq,
                name=f"Industrial Equipment {eq}",
                entity_type="EQUIPMENT",
                description=f"Equipment referenced in {filename}"
            )
            # Create triple connecting document to equipment
            kg_store.add_triple(
                subject=doc_id,
                predicate="MENTIONS_EQUIPMENT",
                obj=eq,
                source_doc=filename
            )

        # Add Work Orders / Reports
        for wo in wo_matches:
            kg_store.add_entity(wo, f"Work Order {wo}", "WORK_ORDER", f"Maintenance record {wo}")
            kg_store.add_triple(doc_id, "CONTAINS_WORK_ORDER", wo, filename)
            for eq in equipment_matches:
                kg_store.add_triple(eq, "SERVICED_UNDER", wo, filename)

        for ir in ir_matches:
            kg_store.add_entity(ir, f"Inspection Report {ir}", "INSPECTION_REPORT", f"Quality inspection {ir}")
            kg_store.add_triple(doc_id, "CONTAINS_INSPECTION", ir, filename)
            for eq in equipment_matches:
                kg_store.add_triple(eq, "INSPECTED_IN", ir, filename)

        for sp in sp_matches:
            kg_store.add_entity(sp, f"Safety Procedure {sp}", "SAFETY_PROCEDURE", f"Safety spec {sp}")
            for eq in equipment_matches:
                kg_store.add_triple(eq, "GOVERNED_BY", sp, filename)

        # Parse Personnel (Technicians / Operators / Inspectors)
        personnel = set(re.findall(r'(?:Technician|Operator|Inspector|By):\s*([A-Z]\.\s*[A-Z][a-z]+)', text))
        for p in personnel:
            p_id = p.replace(".", "").replace(" ", "_").upper()
            kg_store.add_entity(p_id, f"Staff {p}", "PERSON", f"Personnel: {p}")
            kg_store.add_triple(p_id, "EXECUTED_ACTION_IN", doc_id, filename)

        # Parse Parts Used
        parts = set(re.findall(r'Part#\s*([A-Z0-9-]+)', text))
        for pt in parts:
            kg_store.add_entity(pt, f"Spare Part {pt}", "PART", f"Replacement part {pt}")
            for eq in equipment_matches:
                kg_store.add_triple(eq, "USES_PART", pt, filename)
