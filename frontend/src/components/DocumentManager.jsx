import React, { useState, useEffect } from 'react';
import { Upload, Database, FileText, CheckCircle2, RefreshCw, GitFork, Layers } from 'lucide-react';

export default function DocumentManager({ stats, refreshStats }) {
  const [documents, setDocuments] = useState([]);
  const [entities, setEntities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [selectedEntity, setSelectedEntity] = useState(null);
  const [entityTriples, setEntityTriples] = useState([]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const docRes = await fetch('http://localhost:8000/api/documents');
      const docJson = await docRes.json();
      if (docJson.status === 'success') setDocuments(docJson.data);

      const entRes = await fetch('http://localhost:8000/api/entities');
      const entJson = await entRes.json();
      if (entJson.status === 'success') setEntities(entJson.data);
    } catch (err) {
      console.error("Fetch document data error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setUploading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8000/api/ingest/file', {
        method: 'POST',
        body: formData
      });
      const json = await res.json();
      if (json.status === 'success') {
        fetchData();
        if (refreshStats) refreshStats();
      }
    } catch (err) {
      alert("File upload failed: " + err.message);
    } finally {
      setUploading(false);
    }
  };

  const handleSelectEntity = async (entityId) => {
    setSelectedEntity(entityId);
    try {
      const res = await fetch(`http://localhost:8000/api/entities/${entityId}`);
      const json = await res.json();
      if (json.status === 'success') setEntityTriples(json.triples);
    } catch (err) {
      console.error("Entity lookup error:", err);
    }
  };

  return (
    <div style={{ padding: '32px', maxWidth: '1400px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '28px' }}>
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 700, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Database size={26} color="#38bdf8" /> Knowledge Base & Relational Triples
          </h1>
          <p style={{ color: '#94a3b8', fontSize: '0.9rem', marginTop: '4px' }}>
            Ingest heterogeneous engineering drawings, inspection logs, and safety specifications into vector store & SQLite Knowledge Graph.
          </p>
        </div>

        {/* Upload Button */}
        <label style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '10px 18px',
          background: 'linear-gradient(135deg, #38bdf8 0%, #0284c7 100%)',
          borderRadius: '10px',
          color: '#ffffff',
          fontWeight: 600,
          fontSize: '0.85rem',
          cursor: 'pointer',
          boxShadow: '0 4px 14px rgba(56, 189, 248, 0.3)'
        }}>
          <Upload size={16} /> {uploading ? 'Processing Document...' : 'Upload Document'}
          <input type="file" onChange={handleFileUpload} style={{ display: 'none' }} accept=".txt,.pdf,.csv,.xlsx" />
        </label>
      </div>

      {/* Main Content Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '24px' }}>
        {/* Left Panel: Ingested Document Catalog */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3 style={{ fontSize: '1.1rem', color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <FileText size={18} color="#38bdf8" /> Ingested Documents ({documents.length})
            </h3>
            <button onClick={fetchData} style={{ background: 'none', border: 'none', color: '#38bdf8', cursor: 'pointer' }}>
              <RefreshCw size={16} />
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxHeight: '550px', overflowY: 'auto' }}>
            {documents.map((doc, idx) => (
              <div key={idx} style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '12px 16px',
                borderRadius: '8px',
                background: 'rgba(255, 255, 255, 0.02)',
                border: '1px solid rgba(255, 255, 255, 0.06)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <FileText size={18} color="#94a3b8" />
                  <div>
                    <div style={{ fontSize: '0.88rem', fontWeight: 600, color: '#f8fafc', fontFamily: 'JetBrains Mono' }}>
                      {doc.filename}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                      Type: {doc.doc_type} • Chunks: {doc.chunk_count}
                    </div>
                  </div>
                </div>

                <span className="badge-status badge-nominal">
                  <CheckCircle2 size={12} /> INGESTED
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Right Panel: Knowledge Graph Entities & Triples Viewer */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '1.1rem', color: '#f8fafc', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <GitFork size={18} color="#10b981" /> Extracted Entities & Relational Triples
          </h3>

          <div style={{ marginBottom: '16px' }}>
            <div style={{ fontSize: '0.75rem', color: '#94a3b8', uppercase: 'true', marginBottom: '8px' }}>
              Select Entity to Inspect Graph Neighborhood:
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', maxHeight: '120px', overflowY: 'auto' }}>
              {entities.map(ent => (
                <button
                  key={ent.id}
                  onClick={() => handleSelectEntity(ent.id)}
                  style={{
                    padding: '4px 10px',
                    borderRadius: '6px',
                    border: 'none',
                    background: selectedEntity === ent.id ? '#10b981' : 'rgba(255, 255, 255, 0.05)',
                    color: selectedEntity === ent.id ? '#ffffff' : '#cbd5e1',
                    fontSize: '0.75rem',
                    fontFamily: 'JetBrains Mono',
                    cursor: 'pointer'
                  }}
                >
                  {ent.id} ({ent.entity_type})
                </button>
              ))}
            </div>
          </div>

          {/* Triples output list */}
          {selectedEntity && (
            <div style={{ marginTop: '16px', paddingTop: '16px', borderTop: '1px solid rgba(255, 255, 255, 0.08)' }}>
              <div style={{ fontSize: '0.8rem', fontWeight: 600, color: '#38bdf8', marginBottom: '10px' }}>
                Triples linked to {selectedEntity} ({entityTriples.length}):
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '280px', overflowY: 'auto' }}>
                {entityTriples.map((tr, idx) => (
                  <div key={idx} style={{
                    padding: '10px',
                    background: 'rgba(16, 185, 129, 0.08)',
                    border: '1px solid rgba(16, 185, 129, 0.2)',
                    borderRadius: '6px',
                    fontSize: '0.78rem',
                    fontFamily: 'JetBrains Mono',
                    color: '#e2e8f0'
                  }}>
                    <span style={{ color: '#38bdf8' }}>({tr.subject})</span> --[<span style={{ color: '#fbbf24' }}>{tr.predicate}</span>]--&gt; <span style={{ color: '#34d399' }}>({tr.object})</span>
                    <div style={{ fontSize: '0.68rem', color: '#64748b', marginTop: '2px' }}>Source: {tr.source_doc}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
