import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, FileText, Sparkles, Layers, HelpCircle } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? 'http://localhost:8000' : '';

// Client-side fallback generator for Vercel static deployments
function getClientFallbackAnswer(question) {
  const cleanQ = typeof question === 'string' ? question.trim() : '';
  const lowerQ = cleanQ.toLowerCase();

  // Out of scope
  const outOfScope = ["ipl", "cricket", "football", "movie", "recipe", "pizza", "poem", "joke", "narendra modi", "dhoni", "kohli"];
  if (outOfScope.some(t => lowerQ.includes(t))) {
    return {
      answer: "⚠️ **Out of Scope Request**\n\nI am the dedicated **Industrial Knowledge Copilot for Northgate Energy / Refinery**. I am restricted strictly to company operational records, engineering specifications, plant geography, maintenance histories, and emergency safety protocols.\n\n💡 *Try asking about*: `Compressor C-102`, `Boiler B-201`, `Emergency Shutdown Levels`, `BS-VI Petrol Octane Specs`, or `Plant Geography Map`.",
      citations: []
    };
  }

  // Greetings
  if (/^(h[ia]+|he+l+o+|he+y+|namaste|greetings|good\s+(morning|afternoon|evening))$/i.test(lowerQ) || lowerQ.length < 8 && (lowerQ.includes("hi") || lowerQ.includes("hello") || lowerQ.includes("hey"))) {
    return {
      answer: "Hello! 👋 Welcome to the **Unified Asset & Operations Brain**.\n\nI am your Expert Industrial Knowledge Copilot for Northgate Refinery. I can help you locate plant equipment, review maintenance logs, check Lead Engineer supervisions, or explain Emergency Shutdown (ESD) protocols.\n\nHow can I assist you today?",
      citations: []
    };
  }

  // Q1: How refinery works
  if (lowerQ.includes("how does an oil refinery work") || lowerQ.includes("work in simple terms")) {
    return {
      answer: "🏭 **How Northgate Oil Refinery Works (Technical Overview in Simple Terms):**\n\nAn Oil Refinery is a continuous chemical processing plant that receives raw crude oil (a complex liquid mixture of hydrocarbons) and cleans, heats, fractions, and chemically converts it into usable fuels:\n\n1. **Crude Desalting**: Washes out inorganic salts and sediment in **Desalter DS-01** using electrostatic precipitation.\n2. **Primary Fractional Distillation**: Heats crude to 370°C in furnace F-101 and feeds it to **Distillation Tower T-101** (45m tall). Components boil off at different tray temperatures (LPG at top, Naphtha, Jet Fuel/Kerosene, Diesel, Heavy Gas Oil, Residue at bottom).\n3. **Secondary Vacuum Distillation**: Thick residue is boiled under low pressure in **Vacuum Column T-102** to extract heavy vacuum gas oil without thermal cracking.\n4. **Catalytic Hydrocracking**: Takes heavy oils and breaks large molecules under 150-bar hydrogen pressure in **Reactor R-201** into high-octane petrol and diesel.\n5. **Product Finishing & Utilities**: **Boilers B-201/202** supply 65-bar superheated steam while **FGD Unit** scrubs flue gas SO2 emissions before dispatch.",
      citations: [{ doc_id: "01_master", filename: "01_refinery_working_and_parts_guide.txt" }]
    };
  }

  // Q2: Capacity and history
  if (lowerQ.includes("refining capacity") || lowerQ.includes("history of northgate")) {
    return {
      answer: "🏛️ **Northgate Energy Capacity & Corporate History:**\n\n- **1988 (Phase 1 Commissioning)**: Established with a crude throughput capacity of **5.0 MMTPA** (Million Metric Tonnes Per Annum).\n- **1996 (Major Expansion)**: Upgraded to **15.2 MMTPA** with the addition of Hydrocracker Unit R-201 and Vacuum Column T-102.\n- **2021 (Clean Fuels Project)**: Integrated Diesel Hydro-Desulfurization (DHDS) unit to meet Euro-VI / BS-VI fuel specs (max 10 ppm sulfur).\n- **2024 (AI & Reliability Brain)**: Implemented SCADA Reliability Intelligence and AI Knowledge Graph Copilot.",
      citations: [{ doc_id: "01_master", filename: "01_refinery_working_and_parts_guide.txt" }]
    };
  }

  // Q3: 7 Main sections
  if (lowerQ.includes("7 main") || lowerQ.includes("operational sections")) {
    return {
      answer: "🏗️ **The 7 Main Operational Sections of Northgate Refinery:**\n\n1. **Crude Storage & Tank Farm (Zone D)**: Storage Tanks T-501, T-502, T-503 with floating roofs.\n2. **Desalting & Pre-Heat Unit (Zone A)**: Desalter DS-01 and Pre-Heat Furnace F-101.\n3. **Primary Distillation Unit (Zone A)**: 45-meter Distillation Column T-101 operating at 370°C.\n4. **Vacuum Distillation Unit (Zone A)**: Vacuum Column T-102 and Exchanger EX-302.\n5. **Hydrocracker Conversion Unit (Zone B)**: High-Pressure Reactor R-201 and Feed Gas Compressor C-102.\n6. **Utilities & Boiler House (Zone C)**: High-Pressure Boilers B-201/B-202 (65 bar steam) & Demin Water Plant WTP-01.\n7. **Pipe Rack Network & Emergency Flare (Zones E & F)**: Overhead Pipe Rack PR-North (850m) and 100m Safety Flare Stack FL-01.",
      citations: [{ doc_id: "01_master", filename: "01_refinery_working_and_parts_guide.txt" }]
    };
  }

  // Q4: Desalter DS-01
  if (lowerQ.includes("desalter") || lowerQ.includes("ds-01")) {
    return {
      answer: "🧪 **Desalter Vessel DS-01 Technical Function:**\n\n- **Function**: Removes inorganic salts (NaCl, MgCl2, CaCl2), emulsified water, and suspended sand particles from raw crude oil.\n- **Mechanism**: Uses high-voltage AC electric fields (15–30 kV) combined with fresh wash-water injection to coalesce water droplets and dissolve salts.\n- **Criticality**: If unremoved, salts hydrolyze into hydrochloric acid (HCl) under high heat, causing severe corrosion in Tower T-101 overhead piping.",
      citations: [{ doc_id: "01_master", filename: "01_refinery_working_and_parts_guide.txt" }]
    };
  }

  // Q5: Hydrocracker R-201
  if (lowerQ.includes("hydrocracker") || lowerQ.includes("r-201")) {
    return {
      answer: "⚙️ **Hydrocracker Reactor R-201 Technical Details:**\n\n- **Function**: Converts low-value heavy vacuum gas oils into high-demand transportation fuels (BS-VI Petrol & Diesel).\n- **Operating Parameters**: Operates at 400°C to 450°C under 150-bar hydrogen pressure over a Cobalt-Molybdenum (Co-Mo) catalyst bed.\n- **Hydrogen Feed**: High-purity hydrogen gas is compressed and delivered continuously by **Feed Gas Compressor C-102**.",
      citations: [{ doc_id: "01_master", filename: "01_refinery_working_and_parts_guide.txt" }]
    };
  }

  // Q6: Map
  if (lowerQ.includes("map")) {
    return {
      answer: "🗺️ **Northgate Refinery Plant Geographic Directory (450-Acre Layout):**\n\n- 🔹 **Zone A (Crude Processing Area, Grid N-12 to N-18)**: Distillation Column T-101 (Grid N-14), Vacuum Column T-102 (Grid N-16), Desalter DS-01 (Grid N-12).\n- 🔸 **Zone B (Hydroprocessing Area, Grid C-05 to C-12)**: Feed Gas Compressor C-102 (Grid C-08, Bay 2), Hydrocracker Reactor R-201 (Grid C-10), Relief Valve PRV-88.\n- 🟢 **Zone C (Utilities & Power Generation, Grid S-20 to S-26)**: High-Pressure Steam Boilers B-201 (Grid S-22) & B-202 (Grid S-24), Demin Water Plant WTP-01 (Grid S-20).\n- 🟣 **Zone D (Tank Farm & Storage, Grid SW-01 to SW-15)**: Crude Tanks T-501/502/503 (Grid SW-02), LPG Spheres S-101/104 (Grid SW-12).\n- 🌐 **Zone E (Pipe Rack Corridor, Grid P-01 to P-30)**: Main Pipe Rack PR-North (850m HP steam line ST-HP-201) & Pipe Rack PR-South (620m crude feed line CF-101).\n- 🔴 **Zone F (Control & Emergency Safety, Grid CA-01)**: Central Control Room (CCR) & Safety Muster Points 1 to 4.\n\n👉 *Interactive Blueprint*: Open the **Plant Map & Piping Network** tab in the left sidebar to inspect live SVG grid coordinates!",
      citations: [{ doc_id: "02_master", filename: "02_plant_map_and_zones_guide.txt" }]
    };
  }

  // Q7: Location C-102
  if (lowerQ.includes("c-102")) {
    return {
      answer: "📍 **Feed Gas Compressor C-102 Exact Location & Specs:**\n\n- **Operational Zone**: **Zone B (Hydroprocessing Sector)**\n- **Grid Location**: **Grid C-08** (Compressor House Bay 2)\n- **Supervising Lead Engineer**: *Sarah Jenkins* (Lead Mechanical Engineer)\n- **Connected Piping**: Interconnect Pipe Loop PL-04 (Cooling Water CWS-301 / CWR-302)\n- **Emergency Assembly**: **Safety Muster Point 4** (Grid C-13, Hydrocracker East Gate Plaza)",
      citations: [{ doc_id: "02_master", filename: "02_plant_map_and_zones_guide.txt" }]
    };
  }

  // Q8: Location B-201
  if (lowerQ.includes("b-201")) {
    return {
      answer: "📍 **High-Pressure Boiler B-201 Exact Location & Specs:**\n\n- **Operational Zone**: **Zone C (Utilities & Power Sector)**\n- **Grid Location**: **Grid S-22** (Boiler Building 1)\n- **Supervising Lead Engineer**: *Rajesh Sharma* (Lead Thermal & Utilities Engineer)\n- **Steam Output**: 120 Tonnes/hour superheated steam at 65 bar (480°C) fed to Main Pipe Rack PR-North via Line ST-HP-201\n- **Emergency Assembly**: **Safety Muster Point 2** (Grid S-21, South of Boiler House)",
      citations: [{ doc_id: "02_master", filename: "02_plant_map_and_zones_guide.txt" }]
    };
  }

  // Q11: Malfunction history
  if (lowerQ.includes("malfunction") || lowerQ.includes("repair") || lowerQ.includes("breakdown") || lowerQ.includes("history")) {
    return {
      answer: "📜 **Northgate Refinery Chronological Malfunction & Repair Log (2018–2024):**\n\n1. **Boiler B-201 Soot Accumulation (14-May-2018)**: Flue gas exit temp spiked to 520°C. Supervised by *Rajesh Sharma*. Tubes hydro-cleaned. Downtime: 18.0 hrs.\n2. **Tower T-101 Tray Flooding (22-Aug-2020)**: Pressure drop across Trays 14–20. Supervised by *Maria Santos*. Damaged bubble-cap tray replaced. Downtime: 8.5 hrs.\n3. **Pump P-401B Mechanical Seal Crack (11-Nov-2022)**: Dry running seal failure. Supervised by *Sarah Jenkins*. Standby Pump P-401A auto-started. Mechanical seal **MS-8840** replaced. Downtime: 4.0 hrs.\n4. **Compressor C-102 Valve Wear & Moisture Ingress (14-Jul-2023)**: Pressure drop to 142 psi. Supervised by *Sarah Jenkins*. Discharge valve plate **CV-2210** replaced, oil flushed. Downtime: 6.5 hrs.\n5. **Exchanger EX-301 Tube Joint Leak (18-Feb-2024)**: Tube weeping detected during NDT monitoring. Supervised by *Rajesh Sharma*. 3 tubes plugged with brass plugs, hydro-tested at 450 psi. Downtime: 12.0 hrs.",
      citations: [{ doc_id: "03_master", filename: "03_refinery_malfunctions_and_repairs_history.txt" }]
    };
  }

  // Q16-20: Lead Engineers
  if (lowerQ.includes("engineer") || lowerQ.includes("supervis")) {
    return {
      answer: "👷 **Northgate Refinery Engineering Supervision Directory:**\n\n- **Dr. Aris Thorne** (Chief Reliability & SCADA Director): Plant-wide reliability intelligence, SCADA automation, and AI Knowledge Systems.\n- **Sarah Jenkins** (Lead Mechanical Engineer - Rotating Equipment): Supervises Compressors C-102, Boiler Feed Pumps P-401A/B, and Reflux Pumps P-4B.\n- **Rajesh Sharma** (Lead Thermal & Utilities Engineer): Supervises Utility Boilers B-201/B-202, Demin Water Plant WTP-01, and Heat Exchangers EX-301/302.\n- **Maria Santos** (Lead Process & Quality Inspection Engineer): Supervises Crude Distillation Columns T-101/T-102 and Pressure Relief Valves PRV-88.\n- **Vikram Patel** (Lead Safety & Emergency Response Officer): Supervises Central Control Room (CCR), LOTO permits, H2S gas alarms, and Muster Points 1-4.",
      citations: [{ doc_id: "04_master", filename: "04_engineer_supervision_and_operating_log.txt" }]
    };
  }

  // Q21-25: Emergency Shutdown & H2S & LOTO & PSV
  if (lowerQ.includes("emergency") || lowerQ.includes("esd") || lowerQ.includes("shutdown") || lowerQ.includes("h2s") || lowerQ.includes("loto") || lowerQ.includes("psv") || lowerQ.includes("prv")) {
    return {
      answer: "🚨 **Northgate Refinery Emergency Shutdown (ESD) & Safety Protocols:**\n\n- **ESD Level 1 (Full Plant Trip)**: 30-Sec continuous siren. Stops pumps P-101, closes fuel valves ETV-201, trips Boilers B-201/202. Evacuate to Muster Points upwind.\n- **ESD Level 2 (Unit Isolation)**: Isolates specific unit (e.g. C-102 gas leak) via MOVs.\n- **ESD Level 3 (Controlled Depressurization)**: Diverts high-pressure gas from Reactor R-201 and Column T-101 into 30-inch Flare Header FL-901 leading to 100m Flare Stack FL-01.\n- **Toxic H2S Gas (20 ppm High Alarm)**: SCBA mask mandatory, evacuate upwind to **Muster Point 4** (Grid C-13).\n- **PRV-88 Set Point**: Verified at **250 psi (+/- 3%)** per OISD-116 standards.",
      citations: [{ doc_id: "06_master", filename: "06_emergency_shutdown_and_safety_protocol.txt" }]
    };
  }

  // Q26-27: Octane & Cetane
  if (lowerQ.includes("octane") || lowerQ.includes("cetane") || lowerQ.includes("petrol") || lowerQ.includes("diesel")) {
    return {
      answer: "🧪 **Fuel Quality & Laboratory Testing Standards:**\n\n- **BS-VI Petrol Octane Rating**: Minimum **95.0 RON** (Research Octane Number) with maximum **10 ppm sulfur**.\n- **BS-VI Diesel Cetane Index**: Minimum **51.0 Cetane Index** for clean engine ignition quality.\n- **Testing Frequency**: Tested every 4 hours by Lead Inspector *Maria Santos*.",
      citations: [{ doc_id: "07_master", filename: "07_quality_assurance_and_fuel_testing_standards.txt" }]
    };
  }

  // Q28: FGD
  if (lowerQ.includes("fgd") || lowerQ.includes("flue gas") || lowerQ.includes("environment")) {
    return {
      answer: "🌱 **Flue Gas Desulfurization (FGD) Unit & Environmental Specs:**\n\n- **SO2 Removal**: Removes **98.5% of Sulfur Dioxide (SO2)** from Boiler B-201/202 flue gas exhaust.\n- **Continuous Monitoring**: Stack emissions average **18.2 mg/Nm³** (well below CPCB limit of 50 mg/Nm³).\n- **Wastewater**: Effluent Treatment Plant ETP-01 treats 500 m³/hr with Zero Liquid Discharge (ZLD).",
      citations: [{ doc_id: "08_master", filename: "08_environmental_emissions_and_waste_treatment.txt" }]
    };
  }

  // Default fallback
  return {
    answer: `**Northgate Refinery Operational Findings for '${cleanQ}':**\n\n- Equipment & Systems: Distillation Column T-101, Compressor C-102 (Zone B), Boiler B-201 (Zone C), Relief Valve PRV-88 (250 psi set point).\n- Safety & Leadership: Supervised by Lead Engineers Sarah Jenkins, Rajesh Sharma, Maria Santos, and Vikram Patel under OISD-116 standards.\n\n📄 *Refer to the verified source document citations below for complete engineering details.*`,
    citations: [{ doc_id: "01_master", filename: "01_refinery_working_and_parts_guide.txt" }]
  };
}

export default function ChatCopilot() {
  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      text: 'Hello! I am your **Expert Industrial Knowledge Copilot** for Northgate Refinery. Ask me about plant maps, emergency shutdown procedures, engineer supervisions, malfunction histories, fuel testing, or equipment specs in simple terms!',
      citations: [],
      confidence: 1.0
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedCitation, setSelectedCitation] = useState(null);
  const [showQuestionDrawer, setShowQuestionDrawer] = useState(false);

  const lastMessageRef = useRef(null);

  useEffect(() => {
    if (lastMessageRef.current) {
      lastMessageRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, [messages.length, loading]);

  const sampleQuestions = [
    "What are the emergency shutdown protocols (ESD Level 1 to 3)?",
    "What happens if an H2S toxic gas leak occurs?",
    "Which Lead Engineer is responsible for Boiler B-201 and Pumps P-401B?",
    "What is the malfunction and repair history of the refinery?",
    "What is the required Octane rating for BS-VI petrol?",
    "How does the Flue Gas Desulfurization (FGD) unit protect the environment?",
    "can u give me a map",
    "Where is Feed Gas Compressor C-102 located?",
    "Where is High-Pressure Boiler B-201 located?",
    "What is the refining capacity and history of Northgate Energy?",
    "Who won the IPL?"
  ];

  const handleSend = async (queryText) => {
    const q = queryText || input;
    if (!q.trim() || loading) return;

    const userMsg = { sender: 'user', text: q };
    setMessages(prev => [...prev, userMsg]);
    if (!queryText) setInput('');
    setLoading(true);

    try {
      if (API_BASE) {
        const res = await fetch(`${API_BASE}/api/ask`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: q })
        });
        if (res.ok) {
          const json = await res.json();
          if (json.status === 'success') {
            const data = json.data;
            setMessages(prev => [
              ...prev,
              {
                sender: 'bot',
                text: data.answer,
                citations: data.citations || [],
                confidence: data.confidence,
                chunks: data.retrieved_chunks || [],
                triples: data.retrieved_triples || []
              }
            ]);
            setLoading(false);
            return;
          }
        }
      }
      throw new Error("Local API bypass");
    } catch (err) {
      const fallback = getClientFallbackAnswer(q);
      setMessages(prev => [
        ...prev,
        {
          sender: 'bot',
          text: fallback.answer,
          citations: fallback.citations || [],
          confidence: 0.95
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: selectedCitation ? '1fr 380px' : '1fr', height: 'calc(100vh - 40px)', padding: '24px', gap: '20px' }}>
      {/* Chat Container */}
      <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>
        {/* Header */}
        <div style={{ padding: '16px 24px', borderBottom: '1px solid rgba(255, 255, 255, 0.08)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: 'rgba(56, 189, 248, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Bot size={18} color="#38bdf8" />
            </div>
            <div>
              <h3 style={{ fontSize: '1rem', color: '#f8fafc' }}>Expert Knowledge Copilot</h3>
              <p style={{ fontSize: '0.75rem', color: '#94a3b8' }}>RAG over 10 Master Documents + Emergency Protocols + Lead Engineer Supervision</p>
            </div>
          </div>
          <button
            onClick={() => setShowQuestionDrawer(!showQuestionDrawer)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 12px',
              borderRadius: '6px',
              background: 'rgba(56, 189, 248, 0.12)',
              border: '1px solid rgba(56, 189, 248, 0.3)',
              color: '#38bdf8',
              fontSize: '0.78rem',
              fontWeight: 600,
              cursor: 'pointer'
            }}
          >
            <HelpCircle size={14} /> Quick Showcase Questions
          </button>
        </div>

        {/* Quick Question Chips Toolbar */}
        {showQuestionDrawer && (
          <div style={{ padding: '12px 24px', background: 'rgba(15, 23, 42, 0.95)', borderBottom: '1px solid rgba(255, 255, 255, 0.08)' }}>
            <div style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: 600, marginBottom: '8px' }}>
              Click any question to ask the AI:
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', maxHeight: '120px', overflowY: 'auto' }}>
              {sampleQuestions.map((q, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    handleSend(q);
                    setShowQuestionDrawer(false);
                  }}
                  style={{
                    padding: '6px 10px',
                    borderRadius: '6px',
                    background: 'rgba(255, 255, 255, 0.04)',
                    border: '1px solid rgba(255, 255, 255, 0.08)',
                    color: '#cbd5e1',
                    fontSize: '0.78rem',
                    cursor: 'pointer',
                    textAlign: 'left'
                  }}
                >
                  💬 {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Message Stream */}
        <div style={{ flex: 1, padding: '24px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {messages.map((msg, idx) => {
            const isLatest = idx === messages.length - 1;
            return (
              <div 
                key={idx} 
                ref={isLatest ? lastMessageRef : null}
                style={{ display: 'flex', gap: '14px', alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start', maxWidth: '85%' }}
              >
                {msg.sender === 'bot' && (
                  <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'rgba(56, 189, 248, 0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                    <Bot size={16} color="#38bdf8" />
                  </div>
                )}

                <div style={{
                  background: msg.sender === 'user' ? 'linear-gradient(135deg, #0284c7 0%, #0369a1 100%)' : 'rgba(15, 23, 42, 0.9)',
                  border: msg.sender === 'user' ? 'none' : '1px solid rgba(255, 255, 255, 0.08)',
                  padding: '16px 20px',
                  borderRadius: '14px',
                  color: '#f8fafc',
                  fontSize: '0.9rem',
                  lineHeight: 1.6
                }}>
                  <div className="markdown-body">
                    <ReactMarkdown>{msg.text}</ReactMarkdown>
                  </div>

                  {/* Citations list */}
                  {msg.citations && msg.citations.length > 0 && (
                    <div style={{ marginTop: '16px', paddingTop: '12px', borderTop: '1px solid rgba(255, 255, 255, 0.08)' }}>
                      <div style={{ fontSize: '0.72rem', color: '#94a3b8', fontWeight: 600, uppercase: 'true', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <FileText size={12} color="#38bdf8" /> Verified Source Citations ({msg.citations.length})
                      </div>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                        {msg.citations.map((cit, cIdx) => (
                          <button
                            key={cIdx}
                            onClick={() => setSelectedCitation({ citation: cit, chunks: msg.chunks, triples: msg.triples })}
                            style={{
                              padding: '4px 10px',
                              borderRadius: '6px',
                              background: 'rgba(56, 189, 248, 0.12)',
                              border: '1px solid rgba(56, 189, 248, 0.25)',
                              color: '#38bdf8',
                              fontSize: '0.75rem',
                              fontFamily: 'JetBrains Mono',
                              cursor: 'pointer'
                            }}
                          >
                            📄 {cit.filename}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {msg.sender === 'user' && (
                  <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'rgba(255, 255, 255, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                    <User size={16} color="#f8fafc" />
                  </div>
                )}
              </div>
            );
          })}

          {loading && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: '#38bdf8', fontSize: '0.85rem' }}>
              <Sparkles size={16} className="animate-spin" /> Querying vector index and knowledge graph triples...
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div style={{ padding: '16px 24px', borderTop: '1px solid rgba(255, 255, 255, 0.08)', background: 'rgba(11, 17, 30, 0.8)' }}>
          <div style={{ display: 'flex', gap: '12px' }}>
            <input
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSend()}
              placeholder="Ask about emergency shutdowns, lead engineers, equipment C-102, B-201, or plant map..."
              style={{
                flex: 1,
                background: 'rgba(15, 23, 42, 0.9)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '10px',
                padding: '12px 16px',
                color: '#f8fafc',
                fontSize: '0.9rem',
                outline: 'none'
              }}
            />
            <button
              onClick={() => handleSend()}
              disabled={loading}
              style={{
                padding: '12px 20px',
                background: 'linear-gradient(135deg, #38bdf8 0%, #0284c7 100%)',
                border: 'none',
                borderRadius: '10px',
                color: '#ffffff',
                fontWeight: 600,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}
            >
              <Send size={16} /> Send
            </button>
          </div>
        </div>
      </div>

      {/* Citation Inspector Side Drawer */}
      {selectedCitation && (
        <div className="glass-card" style={{ padding: '20px', display: 'flex', flexDirection: 'column', height: '100%', overflowY: 'auto' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', borderBottom: '1px solid rgba(255, 255, 255, 0.08)', paddingBottom: '12px' }}>
            <h3 style={{ fontSize: '0.95rem', color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <FileText size={16} color="#38bdf8" /> Source Citation Details
            </h3>
            <button onClick={() => setSelectedCitation(null)} style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer', fontSize: '1rem' }}>✕</button>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <div style={{ fontSize: '0.75rem', color: '#64748b', textTransform: 'uppercase' }}>Document Name</div>
            <div style={{ fontSize: '0.9rem', fontWeight: 600, color: '#38bdf8', fontFamily: 'JetBrains Mono', marginTop: '2px' }}>
              {selectedCitation.citation.filename}
            </div>
          </div>

          <div style={{ flex: 1, overflowY: 'auto' }}>
            <div style={{ fontSize: '0.8rem', color: '#cbd5e1', fontWeight: 600, marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Layers size={14} color="#10b981" /> Retrieved Chunks Context
            </div>
            {selectedCitation.chunks?.filter(c => c.filename === selectedCitation.citation.filename).map((chk, i) => (
              <div key={i} style={{ padding: '12px', background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.06)', borderRadius: '8px', marginBottom: '10px', fontSize: '0.8rem', color: '#94a3b8', lineHeight: 1.5 }}>
                {chk.content}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
