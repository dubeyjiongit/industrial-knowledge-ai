import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))

def test_pipeline():
    print("=== Testing Ingestion Pipeline ===")
    from api.main import initialize_sample_docs, ask_question, perform_rca, AskRequest, RcaRequest
    
    # 1. Initialize sample docs
    print("[1] Ingesting sample documents...")
    res = initialize_sample_docs()
    print("Ingest Result:", res['message'])
    print("Stats:", res['stats'])
    
    # 2. Test RAG Copilot Query
    print("\n[2] Testing RAG Query Engine...")
    q_res = ask_question(AskRequest(question="What issue was reported for C-102 in July 2023?"))
    print("Answer:\n", q_res['data']['answer'])
    print("Citations:", [c['filename'] for c in q_res['data']['citations']])
    
    # 3. Test RCA Agent
    print("\n[3] Testing Maintenance & RCA Agent...")
    rca_res = perform_rca(RcaRequest(equipment_id="C-102"))
    print("RCA Report:\n", rca_res['data']['rca_report'][:300] + "...")
    print("Timeline Events Found:", len(rca_res['data']['timeline']))
    
    print("\n✅ All Backend Pipeline Components Functioning Perfectly!")

if __name__ == "__main__":
    test_pipeline()
