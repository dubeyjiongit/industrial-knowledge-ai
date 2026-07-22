import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, FileText, Sparkles, Layers, HelpCircle } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? 'http://localhost:8000' : '';

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
      const res = await fetch(`${API_BASE}/api/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q })
      });
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
      }
    } catch (err) {
      setMessages(prev => [
        ...prev,
        {
          sender: 'bot',
          text: '⚠️ Unable to connect to backend server. Make sure the server is running.',
          citations: []
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
