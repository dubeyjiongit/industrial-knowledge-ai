import React from 'react';
import { 
  AlertTriangle, 
  CheckCircle2, 
  FileText, 
  TrendingUp, 
  Wrench, 
  Search,
  ArrowRight,
  ShieldAlert
} from 'lucide-react';

export default function Dashboard({ setActiveTab, stats, onSelectEquipment }) {
  const quickEquipments = [
    { id: 'C-102', name: 'Feed Gas Compressor', type: 'Reciprocating Compressor', status: 'critical', riskScore: '88%', lastWO: 'WO-2023-0847' },
    { id: 'PRV-88', name: 'Pressure Relief Valve', type: 'Safety Valve', status: 'warning', riskScore: '62%', lastWO: 'IR-2023-055' },
    { id: 'P-401B', name: 'Boiler Feed Pump', type: 'Centrifugal Pump', status: 'nominal', riskScore: '14%', lastWO: 'WO-2023-0912' },
    { id: 'T-101', name: 'Distillation Column', type: 'Process Vessel', status: 'nominal', riskScore: '22%', lastWO: 'IR-2024-089' },
  ];

  return (
    <div style={{ padding: '32px', maxWidth: '1400px', margin: '0 auto' }}>
      {/* Header Banner */}
      <div style={{ marginBottom: '32px' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 700, color: '#f8fafc', marginBottom: '8px' }}>
          Industrial Control & Knowledge Dashboard
        </h1>
        <p style={{ color: '#94a3b8', fontSize: '0.95rem' }}>
          Real-time intelligence aggregation across operating procedures, maintenance logs, inspection reports, and safety specs.
        </p>
      </div>

      {/* Metric Cards Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '20px', marginBottom: '32px' }}>
        <div className="glass-card" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
            <span style={{ color: '#94a3b8', fontSize: '0.85rem', fontWeight: 500 }}>Total Documents Ingested</span>
            <FileText size={20} color="#38bdf8" />
          </div>
          <div style={{ fontSize: '2.2rem', fontWeight: 800, color: '#f8fafc' }}>
            {stats?.total_documents || 13}
          </div>
          <div style={{ fontSize: '0.75rem', color: '#10b981', marginTop: '6px', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <TrendingUp size={12} /> 100% Ingestion Complete
          </div>
        </div>

        <div className="glass-card" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
            <span style={{ color: '#94a3b8', fontSize: '0.85rem', fontWeight: 500 }}>Knowledge Graph Triples</span>
            <CheckCircle2 size={20} color="#10b981" />
          </div>
          <div style={{ fontSize: '2.2rem', fontWeight: 800, color: '#38bdf8' }}>
            {stats?.total_triples || 228}
          </div>
          <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '6px' }}>
            Entity relationships linked in SQLite
          </div>
        </div>

        <div className="glass-card" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
            <span style={{ color: '#94a3b8', fontSize: '0.85rem', fontWeight: 500 }}>High Risk Assets</span>
            <ShieldAlert size={20} color="#f43f5e" />
          </div>
          <div style={{ fontSize: '2.2rem', fontWeight: 800, color: '#f43f5e' }}>
            1
          </div>
          <div style={{ fontSize: '0.75rem', color: '#fb7185', marginTop: '6px' }}>
            Compressor C-102 (Monsoon Moisture Risk)
          </div>
        </div>

        <div className="glass-card" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
            <span style={{ color: '#94a3b8', fontSize: '0.85rem', fontWeight: 500 }}>Agentic RCA Status</span>
            <Wrench size={20} color="#f59e0b" />
          </div>
          <div style={{ fontSize: '2.2rem', fontWeight: 800, color: '#f59e0b' }}>
            Active
          </div>
          <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '6px' }}>
            Continuous pattern evaluation
          </div>
        </div>
      </div>

      {/* Main Grid: Equipment Status & Quick Actions */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
        {/* Equipment Risk Monitor */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <div>
              <h3 style={{ fontSize: '1.15rem', color: '#f8fafc' }}>Critical Equipment Intelligence Monitor</h3>
              <p style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Select equipment to launch Root Cause Analysis</p>
            </div>
            <button 
              onClick={() => setActiveTab('rca')}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '8px 14px',
                background: 'rgba(56, 189, 248, 0.12)',
                border: '1px solid rgba(56, 189, 248, 0.3)',
                borderRadius: '8px',
                color: '#38bdf8',
                fontSize: '0.82rem',
                fontWeight: 600,
                cursor: 'pointer'
              }}
            >
              Open RCA Agent <ArrowRight size={14} />
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {quickEquipments.map(eq => (
              <div 
                key={eq.id}
                onClick={() => {
                  onSelectEquipment(eq.id);
                  setActiveTab('rca');
                }}
                className="glass-card-interactive"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '16px',
                  borderRadius: '10px',
                  background: 'rgba(255, 255, 255, 0.02)',
                  cursor: 'pointer'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                  <div style={{
                    padding: '10px 14px',
                    borderRadius: '8px',
                    background: 'rgba(15, 23, 42, 0.8)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    fontFamily: 'JetBrains Mono',
                    fontWeight: 700,
                    color: '#38bdf8'
                  }}>
                    {eq.id}
                  </div>
                  <div>
                    <h4 style={{ fontSize: '0.95rem', color: '#f8fafc', marginBottom: '2px' }}>{eq.name}</h4>
                    <p style={{ fontSize: '0.78rem', color: '#64748b' }}>{eq.type} • Last WO: {eq.lastWO}</p>
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '0.72rem', color: '#64748b', textTransform: 'uppercase' }}>Failure Index</div>
                    <div style={{ fontSize: '0.95rem', fontWeight: 700, color: eq.status === 'critical' ? '#f43f5e' : (eq.status === 'warning' ? '#f59e0b' : '#10b981') }}>
                      {eq.riskScore}
                    </div>
                  </div>
                  <span className={`badge-status badge-${eq.status}`}>
                    {eq.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Copilot Search Prompts */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '1.15rem', color: '#f8fafc', marginBottom: '12px' }}>
            Instant Knowledge Copilot
          </h3>
          <p style={{ fontSize: '0.82rem', color: '#94a3b8', marginBottom: '20px' }}>
            Ask natural language questions to search through all 13 ingested refinery documents:
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {[
              "What issue was reported for C-102 in July 2023?",
              "When is the next inspection due for PRV-88?",
              "What are the safety procedures for compressor startup?",
              "Which parts were replaced during monsoon maintenance?"
            ].map((q, idx) => (
              <button
                key={idx}
                onClick={() => setActiveTab('copilot')}
                style={{
                  padding: '12px',
                  borderRadius: '8px',
                  border: '1px solid rgba(255, 255, 255, 0.06)',
                  background: 'rgba(255, 255, 255, 0.02)',
                  color: '#cbd5e1',
                  fontSize: '0.82rem',
                  textAlign: 'left',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  transition: 'all 0.2s ease'
                }}
              >
                <Search size={14} color="#38bdf8" />
                <span>{q}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
