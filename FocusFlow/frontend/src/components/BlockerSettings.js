import { useState, useEffect } from 'react';

const API_BASE = 'http://localhost:8081/api';

function BlockerSettings({ onSave }) {
  const [blockedSites, setBlockedSites] = useState([]); // array of Rule objects
  const [newApp, setNewApp] = useState('');

  useEffect(() => {
    // load current blocklist from backend
    fetch(`${API_BASE}/rules`)
      .then(r => r.json())
      .then(rules => {
        // Filter only APP blacklist rules
        const appRules = rules.filter(rule => 
          rule.targetType === 'APP' && rule.type === 'BLACKLIST'
        );
        setBlockedSites(appRules);
      })
      .catch(err => {
        console.error('Failed to load rules:', err);
      });
  }, []);

  const saveBlocklist = async (appName) => {
    try {
      // Create a new rule in the backend
      const response = await fetch(`${API_BASE}/rules`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type: 'BLACKLIST',
          targetType: 'APP',
          pattern: appName,
          enabled: true
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      const savedRule = await response.json();
      if (onSave) onSave(savedRule);
      return savedRule;
    } catch (err) {
      // keep UI responsive but let the user know
      alert('Failed to save block list: ' + err.message);
      throw err;
    }
  };

  const handleAdd = async () => {
    const app = (newApp || '').trim();
    if (!app) return;
    
    // Check if already exists
    if (blockedSites.some(rule => rule.pattern === app)) {
      alert('This app is already in the block list.');
      setNewApp('');
      return;
    }
    
    try {
      const savedRule = await saveBlocklist(app);
      setBlockedSites([...blockedSites, savedRule]);
      setNewApp('');
    } catch (err) {
      // Error already shown in saveBlocklist
    }
  };

  const handleRemove = async (rule) => {
    try {
      const response = await fetch(`${API_BASE}/rules/${rule.id}`, {
        method: 'DELETE'
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      setBlockedSites(blockedSites.filter(r => r.id !== rule.id));
    } catch (err) {
      alert('Failed to remove app: ' + err.message);
    }
  };

  const publishBlocklist = async () => {
    try {
      // Push all rules to connected clients
      const res = await fetch(`${API_BASE}/rules/push`, { method: 'POST' });
      const data = await res.json();
      
      if (res.ok) {
        alert(`Published block list to ${data.count || 0} connected client(s).`);
      } else {
        alert('Failed to publish block list.');
      }
    } catch (err) {
      alert('Failed to publish block list: ' + err.message);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: 8 }}>
        <input
          type="text"
          placeholder="Add app or process name to block"
          value={newApp}
          onChange={(e) => setNewApp(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter') handleAdd(); }}
        />
        <button onClick={handleAdd} style={{ marginLeft: 8 }}>Add App</button>
      </div>

      <div>
        <h4>Blocked apps / processes</h4>
        {blockedSites.length === 0 ? (
          <p><em>No apps added yet.</em></p>
        ) : (
          <ul>
            {blockedSites.map((rule) => (
              <li key={rule.id} style={{ marginBottom: 6 }}>
                {rule.pattern}
                <button onClick={() => handleRemove(rule)} style={{ marginLeft: 8 }}>Remove</button>
              </li>
            ))}
          </ul>
        )}
        <p style={{ fontSize: 12, color: '#666' }}>Entries are saved automatically and used by the native blocker.</p>
        <div style={{ marginTop: 8 }}>
          <button onClick={publishBlocklist}>Publish</button>
        </div>
      </div>
    </div>
  );
}

export default BlockerSettings;
