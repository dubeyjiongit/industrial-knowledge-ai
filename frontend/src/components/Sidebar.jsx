import React from 'react';
import { 
  Activity, 
  Bot, 
  Wrench, 
  Database, 
  Compass,
  ShieldCheck
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, stats }) {
  const navItems = [
    { id: 'dashboard', label: 'Control Overview', icon: Activity },
    { id: 'copilot', label: 'Expert RAG Copilot', icon: Bot },
    { id: 'rca', label: 'Maintenance & RCA Agent', icon: Wrench },
    { id: 'map', label: 'Plant Map & Piping Network', icon: Compass },
    { id: 'documents', label: 'Knowledge Base & Graph', icon: Database },
  ];

  return (
    <aside style={{
      width: '260px',
      height: '100vh',
      position: 'fixed',
      left: 0,
      top: 0,
      backgroundColor: 'rgba(11, 17, 30, 0.95)',
      borderRight: '1px solid rgba(255, 255, 255, 0.08)',
      display: 'flex',
      flexDirection: 'column',
      zIndex: 50,
      backdropFilter: 'blur(16px)'
    }}>
      {/* Brand Header */}
      <div style={{ padding: '24px 20px', borderBottom: '1px solid rgba(255, 255, 255, 0.08)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
          <div style={{
            width: '36px',
            height: '36px',
            borderRadius: '10px',
            background: 'linear-gradient(135deg, #38bdf8 0%, #0284c7 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 16px rgba(56, 189, 248, 0.4)'
          }}>
            <ShieldCheck size={22} color="#ffffff" />
          </div>
          <div>
            <h2 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc', letterSpacing: '-0.02em' }}>
              NORTHGATE
            </h2>
            <p style={{ fontSize: '0.68rem', color: '#38bdf8', fontWeight: 600, letterSpacing: '0.08em' }}>
              INDUSTRIAL ASSET BRAIN
            </p>
          </div>
        </div>

        {/* Live Facility Badge */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '6px 10px',
          background: 'rgba(16, 185, 129, 0.1)',
          border: '1px solid rgba(16, 185, 129, 0.25)',
          borderRadius: '6px',
          fontSize: '0.72rem',
          color: '#34d399',
          marginTop: '12px'
        }}>
          <span className="live-dot"></span>
          <span style={{ fontWeight: 600 }}>NORTHGATE REFINERY — UNIT 3</span>
        </div>
      </div>

      {/* Navigation Links */}
      <nav style={{ padding: '16px 12px', flex: 1, display: 'flex', flexDirection: 'column', gap: '6px' }}>
        {navItems.map(item => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px 14px',
                borderRadius: '8px',
                border: 'none',
                background: isActive ? 'linear-gradient(90deg, rgba(56, 189, 248, 0.18) 0%, rgba(56, 189, 248, 0.05) 100%)' : 'transparent',
                color: isActive ? '#38bdf8' : '#94a3b8',
                fontWeight: isActive ? 600 : 400,
                fontSize: '0.88rem',
                cursor: 'pointer',
                textAlign: 'left',
                borderLeft: isActive ? '3px solid #38bdf8' : '3px solid transparent',
                transition: 'all 0.2s ease'
              }}
            >
              <Icon size={18} color={isActive ? '#38bdf8' : '#64748b'} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Footer Stats Summary */}
      <div style={{ padding: '16px', borderTop: '1px solid rgba(255, 255, 255, 0.08)', background: 'rgba(15, 23, 42, 0.6)' }}>
        <div style={{ fontSize: '0.72rem', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '8px' }}>
          Graph Storage Metrics
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
          <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '8px', borderRadius: '6px', textAlign: 'center' }}>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc' }}>
              {stats?.total_documents || 10}
            </div>
            <div style={{ fontSize: '0.65rem', color: '#94a3b8' }}>Documents</div>
          </div>
          <div style={{ background: 'rgba(255, 255, 255, 0.03)', padding: '8px', borderRadius: '6px', textAlign: 'center' }}>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#38bdf8' }}>
              {stats?.total_triples || 150}
            </div>
            <div style={{ fontSize: '0.65rem', color: '#94a3b8' }}>KG Triples</div>
          </div>
        </div>
      </div>
    </aside>
  );
}
