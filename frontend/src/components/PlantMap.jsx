import React, { useState } from 'react';
import { MapPin, Navigation, Shield, Compass, Layers, AlertCircle } from 'lucide-react';

export default function PlantMap() {
  const [selectedZone, setSelectedZone] = useState('ZONE_C');

  const zones = {
    ZONE_A: {
      name: 'Zone A: Crude Processing Area',
      grid: 'North-West Sector (Grid N-12 to N-18)',
      color: '#38bdf8',
      equipments: [
        { id: 'T-101', name: 'Distillation Column', desc: 'Main crude fractionation tower connected to Pipe Rack PR-North at Grid N-14.' },
        { id: 'T-102', name: 'Vacuum Column', desc: 'Heavy distillate column at Grid N-16 connected to Condenser EX-302.' },
        { id: 'DS-01', name: 'Desalter Unit', desc: 'Raw crude desalting vessel at Grid N-12.' }
      ]
    },
    ZONE_B: {
      name: 'Zone B: Hydroprocessing Area',
      grid: 'Central Sector (Grid C-05 to C-12)',
      color: '#f59e0b',
      equipments: [
        { id: 'C-102', name: 'Feed Gas Compressor', desc: 'Reciprocating Compressor in Compressor House Bay 2 (Grid C-08).' },
        { id: 'R-201', name: 'Hydrocracker Reactor', desc: 'High-pressure conversion vessel at Grid C-10.' },
        { id: 'PRV-88', name: 'Pressure Relief Valve', desc: 'Safety valve on T-101 manifold at Grid C-06, Height 14m.' }
      ]
    },
    ZONE_C: {
      name: 'Zone C: Utilities & Boiler House',
      grid: 'South-East Sector (Grid S-20 to S-26)',
      color: '#10b981',
      equipments: [
        { id: 'B-201', name: 'High-Pressure Steam Boiler 1', desc: '120 T/h 65-bar natural gas/RFG boiler at Grid S-22.' },
        { id: 'B-202', name: 'High-Pressure Steam Boiler 2', desc: '120 T/h dual-fired boiler at Grid S-24.' },
        { id: 'WTP-01', name: 'Water Demineralization Plant', desc: 'High-purity boiler feedwater plant at Grid S-20.' }
      ]
    },
    ZONE_D: {
      name: 'Zone D: Tank Farm & Storage',
      grid: 'South-West Sector (Grid SW-01 to SW-15)',
      color: '#a855f7',
      equipments: [
        { id: 'T-501 to T-503', name: 'Crude Storage Tanks', desc: 'Floating roof storage tanks at Grid SW-02 to SW-06.' },
        { id: 'S-101 to S-104', name: 'LPG Spheres', desc: 'Pressurized gas storage spheres at Grid SW-12.' },
        { id: 'CS-03', name: 'Chemical Dosing Station', desc: 'Corrosion inhibitor station at Grid SW-15.' }
      ]
    },
    ZONE_E: {
      name: 'Zone E: Piping & Interconnect Network',
      grid: 'Arterial Corridor (Grid P-01 to P-30)',
      color: '#06b6d4',
      equipments: [
        { id: 'PR-North', name: 'Main Pipe Rack North', desc: '850m overhead pipe rack carrying 65-bar HP steam (ST-HP-201) to process units.' },
        { id: 'PR-South', name: 'Main Pipe Rack South', desc: '620m pipe rack connecting Tank Farm to Hydrocracker.' },
        { id: 'PL-04', name: 'Interconnect Pipe Loop', desc: 'Overhead cooling water bridge crossing Access Road 3.' }
      ]
    },
    ZONE_F: {
      name: 'Zone F: Control & Safety Centre',
      grid: 'Central Admin Grid CA-01',
      color: '#f43f5e',
      equipments: [
        { id: 'CCR', name: 'Central Control Room', desc: 'Blast-resistant main plant control center at Grid CA-01.' },
        { id: 'Muster Point 1', name: 'Main Gate Assembly Plaza', desc: 'Primary evacuation point for Admin and Visitors (Grid CA-05).' },
        { id: 'Muster Point 2', name: 'Boiler House Assembly Point', desc: 'Primary evacuation point for Zone C personnel (Grid S-21).' },
        { id: 'Muster Point 3/4', name: 'Tank Farm & Hydrocracker Points', desc: 'Muster Point 3 (Grid SW-01) and Muster Point 4 (Grid C-13).' }
      ]
    }
  };

  const activeZoneData = zones[selectedZone];

  return (
    <div style={{ padding: '32px', maxWidth: '1400px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '28px' }}>
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 700, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Compass size={26} color="#38bdf8" /> Northgate Refinery — Interactive Facility Map & Piping Layout
          </h1>
          <p style={{ color: '#94a3b8', fontSize: '0.9rem', marginTop: '4px' }}>
            Geographic coordinates, zone layouts, pipe rack corridors, boiler houses, and safety muster points.
          </p>
        </div>
      </div>

      {/* Grid Layout */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: '24px' }}>
        {/* Interactive Visual Blueprint Map */}
        <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <div style={{ width: '100%', display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <span style={{ fontSize: '0.85rem', color: '#94a3b8', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Navigation size={16} color="#38bdf8" /> Industrial Grid Blueprint (450 Acres)
            </span>
            <span style={{ fontSize: '0.75rem', color: '#10b981', fontFamily: 'JetBrains Mono' }}>GPS: 22.3072° N, 73.1812° E</span>
          </div>

          {/* SVG Map Canvas */}
          <div style={{ width: '100%', background: 'rgba(5, 10, 20, 0.9)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.08)', padding: '20px', position: 'relative' }}>
            <svg viewBox="0 0 800 500" style={{ width: '100%', height: 'auto' }}>
              {/* Grid Background Lines */}
              <defs>
                <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                  <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.04)" strokeWidth="1" />
                </pattern>
              </defs>
              <rect width="800" height="500" fill="url(#grid)" />

              {/* Main Pipe Rack PR-North Connection Line */}
              <path d="M 180 140 L 620 340" stroke="#06b6d4" strokeWidth="4" strokeDasharray="6 4" />
              <text x="380" y="220" fill="#06b6d4" fontSize="11" fontFamily="JetBrains Mono" fontWeight="bold">Main Pipe Rack PR-North (850m HP Steam)</text>

              {/* Pipe Rack PR-South Connection Line */}
              <path d="M 180 340 L 400 180" stroke="#a855f7" strokeWidth="3" strokeDasharray="4 4" />
              <text x="240" y="290" fill="#a855f7" fontSize="10" fontFamily="JetBrains Mono">PR-South (Crude Feed Line)</text>

              {/* ZONE A: Northwest */}
              <g onClick={() => setSelectedZone('ZONE_A')} style={{ cursor: 'pointer' }}>
                <rect x="60" y="50" width="240" height="150" rx="10" 
                      fill={selectedZone === 'ZONE_A' ? 'rgba(56, 189, 248, 0.25)' : 'rgba(15, 23, 42, 0.8)'} 
                      stroke="#38bdf8" strokeWidth={selectedZone === 'ZONE_A' ? '3' : '1.5'} />
                <text x="80" y="85" fill="#38bdf8" fontSize="14" fontWeight="bold">ZONE A: Crude Processing</text>
                <text x="80" y="110" fill="#cbd5e1" fontSize="11">T-101 Distillation Tower</text>
                <text x="80" y="130" fill="#cbd5e1" fontSize="11">T-102 Vacuum Column</text>
                <circle cx="260" cy="140" r="14" fill="#38bdf8" />
                <text x="254" y="144" fill="#000" fontSize="10" fontWeight="bold">N-14</text>
              </g>

              {/* ZONE B: Central Hydrocracker */}
              <g onClick={() => setSelectedZone('ZONE_B')} style={{ cursor: 'pointer' }}>
                <rect x="340" y="70" width="220" height="150" rx="10" 
                      fill={selectedZone === 'ZONE_B' ? 'rgba(245, 158, 11, 0.25)' : 'rgba(15, 23, 42, 0.8)'} 
                      stroke="#f59e0b" strokeWidth={selectedZone === 'ZONE_B' ? '3' : '1.5'} />
                <text x="360" y="105" fill="#f59e0b" fontSize="14" fontWeight="bold">ZONE B: Hydroprocessing</text>
                <text x="360" y="130" fill="#cbd5e1" fontSize="11">Compressor C-102 (Bay 2)</text>
                <text x="360" y="150" fill="#cbd5e1" fontSize="11">Valve PRV-88 (14m Height)</text>
                <circle cx="520" cy="140" r="14" fill="#f59e0b" />
                <text x="513" y="144" fill="#000" fontSize="10" fontWeight="bold">C-08</text>
              </g>

              {/* ZONE C: Boiler House & Utilities */}
              <g onClick={() => setSelectedZone('ZONE_C')} style={{ cursor: 'pointer' }}>
                <rect x="520" y="270" width="230" height="180" rx="10" 
                      fill={selectedZone === 'ZONE_C' ? 'rgba(16, 185, 129, 0.25)' : 'rgba(15, 23, 42, 0.8)'} 
                      stroke="#10b981" strokeWidth={selectedZone === 'ZONE_C' ? '3' : '1.5'} />
                <text x="540" y="305" fill="#10b981" fontSize="14" fontWeight="bold">ZONE C: Boiler House</text>
                <text x="540" y="330" fill="#cbd5e1" fontSize="11">Boiler B-201 (65 bar, 480°C)</text>
                <text x="540" y="350" fill="#cbd5e1" fontSize="11">Boiler B-202 (Dual Fired)</text>
                <text x="540" y="370" fill="#cbd5e1" fontSize="11">Demin Water Plant WTP-01</text>
                <circle cx="710" cy="340" r="14" fill="#10b981" />
                <text x="702" y="344" fill="#000" fontSize="10" fontWeight="bold">S-22</text>
              </g>

              {/* ZONE D: Tank Farm */}
              <g onClick={() => setSelectedZone('ZONE_D')} style={{ cursor: 'pointer' }}>
                <rect x="60" y="270" width="220" height="180" rx="10" 
                      fill={selectedZone === 'ZONE_D' ? 'rgba(168, 85, 247, 0.25)' : 'rgba(15, 23, 42, 0.8)'} 
                      stroke="#a855f7" strokeWidth={selectedZone === 'ZONE_D' ? '3' : '1.5'} />
                <text x="80" y="305" fill="#a855f7" fontSize="14" fontWeight="bold">ZONE D: Tank Farm</text>
                <text x="80" y="330" fill="#cbd5e1" fontSize="11">Crude Tanks T-501 to T-503</text>
                <text x="80" y="350" fill="#cbd5e1" fontSize="11">LPG Spheres S-101 to S-104</text>
                <circle cx="240" cy="340" r="14" fill="#a855f7" />
                <text x="230" y="344" fill="#000" fontSize="10" fontWeight="bold">SW-02</text>
              </g>

              {/* ZONE F: Central Control & Safety */}
              <g onClick={() => setSelectedZone('ZONE_F')} style={{ cursor: 'pointer' }}>
                <rect x="340" y="270" width="150" height="180" rx="10" 
                      fill={selectedZone === 'ZONE_F' ? 'rgba(244, 63, 94, 0.25)' : 'rgba(15, 23, 42, 0.8)'} 
                      stroke="#f43f5e" strokeWidth={selectedZone === 'ZONE_F' ? '3' : '1.5'} />
                <text x="355" y="305" fill="#f43f5e" fontSize="13" fontWeight="bold">ZONE F: CCR & Safety</text>
                <text x="355" y="330" fill="#cbd5e1" fontSize="10">Control Room (CA-01)</text>
                <text x="355" y="350" fill="#fb7185" fontSize="10">Muster Points 1-4</text>
                <text x="355" y="370" fill="#cbd5e1" fontSize="10">Main Fire Station</text>
              </g>
            </svg>
          </div>
        </div>

        {/* Zone Details Sidebar */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px', borderBottom: '1px solid rgba(255,255,255,0.08)', paddingBottom: '12px' }}>
            <MapPin size={22} color={activeZoneData.color} />
            <div>
              <h3 style={{ fontSize: '1.1rem', color: '#f8fafc' }}>{activeZoneData.name}</h3>
              <p style={{ fontSize: '0.78rem', color: '#94a3b8', fontFamily: 'JetBrains Mono' }}>{activeZoneData.grid}</p>
            </div>
          </div>

          <div style={{ fontSize: '0.82rem', color: '#cbd5e1', fontWeight: 600, uppercase: 'true', marginBottom: '12px' }}>
            Equipment & Piping Assets in this Zone:
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {activeZoneData.equipments.map((eq, idx) => (
              <div key={idx} style={{
                padding: '14px',
                borderRadius: '8px',
                background: 'rgba(255, 255, 255, 0.02)',
                border: `1px solid ${activeZoneData.color}40`,
                borderLeft: `4px solid ${activeZoneData.color}`
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                  <span style={{ fontSize: '0.9rem', fontWeight: 700, color: '#f8fafc', fontFamily: 'JetBrains Mono' }}>
                    {eq.id}
                  </span>
                  <span style={{ fontSize: '0.75rem', fontWeight: 600, color: activeZoneData.color }}>
                    {eq.name}
                  </span>
                </div>
                <p style={{ fontSize: '0.8rem', color: '#94a3b8', lineHeight: 1.4 }}>
                  {eq.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
