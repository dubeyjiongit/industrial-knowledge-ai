import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import ChatCopilot from './components/ChatCopilot';
import RcaAgent from './components/RcaAgent';
import PlantMap from './components/PlantMap';
import DocumentManager from './components/DocumentManager';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [stats, setStats] = useState(null);
  const [selectedEquipment, setSelectedEquipment] = useState('C-102');

  const fetchStats = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/stats');
      const json = await res.json();
      if (json.status === 'success') {
        setStats(json.data);
      }
    } catch (err) {
      console.log("Stats fetch notice: API server not reachable yet.");
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  return (
    <div style={{ display: 'flex', minHeight: '100vh', backgroundColor: '#090d16' }}>
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} stats={stats} />

      <main style={{ flex: 1, marginLeft: '260px', width: 'calc(100% - 260px)', minHeight: '100vh' }}>
        {activeTab === 'dashboard' && (
          <Dashboard 
            setActiveTab={setActiveTab} 
            stats={stats} 
            onSelectEquipment={setSelectedEquipment} 
          />
        )}

        {activeTab === 'copilot' && (
          <ChatCopilot />
        )}

        {activeTab === 'rca' && (
          <RcaAgent 
            selectedEquipment={selectedEquipment} 
            setSelectedEquipment={setSelectedEquipment} 
          />
        )}

        {activeTab === 'map' && (
          <PlantMap />
        )}

        {activeTab === 'documents' && (
          <DocumentManager 
            stats={stats} 
            refreshStats={fetchStats} 
          />
        )}
      </main>
    </div>
  );
}
