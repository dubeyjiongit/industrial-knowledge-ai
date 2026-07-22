import React, { useState, useEffect } from 'react';
import { Wrench, Calendar, AlertOctagon, CheckCircle2, ShieldAlert, Sparkles, RefreshCw } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export default function RcaAgent({ selectedEquipment, setSelectedEquipment }) {
  const [equipmentId, setEquipmentId] = useState(selectedEquipment || 'C-102');
  const [loading, setLoading] = useState(false);
  const [rcaData, setRcaData] = useState(null);

  const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? 'http://localhost:8000' : '';

  const availableEquipments = ['C-102', 'PRV-88', 'P-401B', 'T-101', 'EX-301'];

  const runAnalysis = async (targetId) => {
    const idToUse = targetId || equipmentId;
    if (!idToUse) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/rca`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ equipment_id: idToUse })
      });
      const json = await res.json();
      if (json.status === 'success') {
        setRcaData(json.data);
      }
    } catch (err) {
      console.error("RCA agent request failed:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runAnalysis(equipmentId);
  }, []);

  return (
    <div style={{ padding: '32px', maxWidth: '1400px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '28px' }}>
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 700, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Wrench size={26} color="#f59e0b" /> Maintenance & Root Cause Analysis Agent
          </h1>
          <p style={{ color: '#94a3b8', fontSize: '0.9rem', marginTop: '4px' }}>
            Autonomous reliability pattern extraction over equipment maintenance history & inspection findings.
          </p>
        </div>

        {/* Equipment Selector */}
        <div style={{ display: 'flex', gap: '8px', background: 'rgba(15, 23, 42, 0.8)', padding: '6px', borderRadius: '10px', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
          {availableEquipments.map(eq => (
            <button
              key={eq}
              onClick={() => {
                setEquipmentId(eq);
                if (setSelectedEquipment) setSelectedEquipment(eq);
                runAnalysis(eq);
              }}
              style={{
                padding: '8px 14px',
                borderRadius: '6px',
                border: 'none',
                background: equipmentId === eq ? 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)' : 'transparent',
                color: equipmentId === eq ? '#ffffff' : '#94a3b8',
                fontWeight: 700,
                fontFamily: 'JetBrains Mono',
                fontSize: '0.85rem',
                cursor: 'pointer'
              }}
            >
              {eq}
            </button>
          ))}
        </div>
      </div>

      {loading && (
        <div className="glass-card" style={{ padding: '40px', textAlign: 'center', color: '#f59e0b' }}>
          <RefreshCw size={28} className="animate-spin" style={{ margin: '0 auto 12px auto', display: 'block' }} />
          <h3 style={{ fontSize: '1.1rem', color: '#f8fafc' }}>Running Agentic RCA Reasoning on {equipmentId}...</h3>
          <p style={{ fontSize: '0.82rem', color: '#94a3b8', marginTop: '4px' }}>Synthesizing maintenance logs, inspection findings, and KG relational triples.</p>
        </div>
      )}

      {!loading && rcaData && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.3fr', gap: '24px' }}>
          {/* Left Panel: Chronological Maintenance Timeline */}
          <div className="glass-card" style={{ padding: '24px' }}>
            <h3 style={{ fontSize: '1.1rem', color: '#f8fafc', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Calendar size={18} color="#38bdf8" /> Operational Timeline ({rcaData.timeline?.length} Records)
            </h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', position: 'relative', paddingLeft: '16px' }}>
              {/* Vertical line connector */}
              <div style={{ position: 'absolute', left: '6px', top: '10px', bottom: '10px', width: '2px', background: 'rgba(56, 189, 248, 0.2)' }}></div>

              {rcaData.timeline?.map((ev, idx) => (
                <div key={idx} style={{ position: 'relative', paddingLeft: '20px' }}>
                  {/* Timeline dot */}
                  <div style={{
                    position: 'absolute',
                    left: '-14px',
                    top: '4px',
                    width: '10px',
                    height: '10px',
                    borderRadius: '50%',
                    background: '#38bdf8',
                    border: '2px solid #090d16'
                  }}></div>

                  <div style={{
                    background: 'rgba(255, 255, 255, 0.02)',
                    border: '1px solid rgba(255, 255, 255, 0.06)',
                    borderRadius: '8px',
                    padding: '12px 16px'
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                      <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#38bdf8', fontFamily: 'JetBrains Mono' }}>
                        📅 {ev.date}
                      </span>
                      <span style={{ fontSize: '0.7rem', color: '#64748b', fontFamily: 'JetBrains Mono' }}>
                        {ev.document}
                      </span>
                    </div>
                    <div style={{ fontSize: '0.85rem', color: '#e2e8f0', lineHeight: 1.4 }}>
                      {ev.summary}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Right Panel: Agentic Root Cause Analysis Report */}
          <div className="glass-card" style={{ padding: '24px', borderLeft: '3px solid #f59e0b' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', borderBottom: '1px solid rgba(255, 255, 255, 0.08)', paddingBottom: '12px' }}>
              <h3 style={{ fontSize: '1.15rem', color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <ShieldAlert size={20} color="#f59e0b" /> RCA & Reliability Report: {rcaData.equipment_id}
              </h3>
              <span className="badge-status badge-warning">LLM REASONED</span>
            </div>

            <div className="markdown-body" style={{ fontSize: '0.9rem', lineHeight: 1.6 }}>
              <ReactMarkdown>{rcaData.rca_report}</ReactMarkdown>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
