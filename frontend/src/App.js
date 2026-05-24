import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API = 'http://127.0.0.1:8000/api';

function App() {
  const [records, setRecords] = useState([]);
  const [stats, setStats] = useState({});
  const [sourceFilter, setSourceFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchStats();
    fetchRecords();
  }, [sourceFilter, statusFilter]);

  const fetchStats = async () => {
    const res = await axios.get(`${API}/stats/`);
    setStats(res.data);
  };

  const fetchRecords = async () => {
    let url = `${API}/records/?`;
    if (sourceFilter) url += `source_type=${sourceFilter}&`;
    if (statusFilter) url += `status=${statusFilter}`;
    const res = await axios.get(url);
    setRecords(res.data);
  };

  const handleUpload = async (e, sourceType) => {
    const file = e.target.files[0];
    if (!file) return;
    setUploading(true);
    setMessage('');
    const formData = new FormData();
    formData.append('file', file);
    formData.append('source_type', sourceType);
    formData.append('client_id', 1);
    try {
      const res = await axios.post(`${API}/upload/`, formData);
      setMessage(`✅ Uploaded! ${res.data.rows_created} rows created.`);
      fetchStats();
      fetchRecords();
    } catch (err) {
      setMessage('❌ Upload failed. Check your CSV format.');
    }
    setUploading(false);
  };

  const handleReview = async (id, status) => {
    await axios.patch(`${API}/records/${id}/review/`, { status });
    fetchStats();
    fetchRecords();
  };

  const statusColor = (status) => {
    if (status === 'APPROVED') return '#22c55e';
    if (status === 'FLAGGED') return '#f59e0b';
    if (status === 'REJECTED') return '#ef4444';
    return '#6b7280';
  };

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', maxWidth: 1200, margin: '0 auto', padding: 24 }}>

      <div style={{ background: '#1e3a5f', color: 'white', padding: 24, borderRadius: 8, marginBottom: 24 }}>
        <h1 style={{ margin: 0 }}>🌱 Breathe ESG — Emissions Dashboard</h1>
        <p style={{ margin: '8px 0 0', opacity: 0.8 }}>Ingest, normalize, and review emissions data</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        {[
          { label: 'Total Records', value: stats.total || 0, color: '#1e3a5f' },
          { label: 'Pending', value: stats.pending || 0, color: '#6b7280' },
          { label: 'Approved', value: stats.approved || 0, color: '#22c55e' },
          { label: 'Flagged', value: stats.flagged || 0, color: '#f59e0b' },
        ].map(s => (
          <div key={s.label} style={{ background: s.color, color: 'white', padding: 20, borderRadius: 8, textAlign: 'center' }}>
            <div style={{ fontSize: 32, fontWeight: 'bold' }}>{s.value}</div>
            <div style={{ opacity: 0.9 }}>{s.label}</div>
          </div>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 24 }}>
        {[
          { label: 'Scope 1 (Direct)', value: stats.scope1_kgco2e || 0 },
          { label: 'Scope 2 (Electricity)', value: stats.scope2_kgco2e || 0 },
          { label: 'Scope 3 (Travel)', value: stats.scope3_kgco2e || 0 },
        ].map(s => (
          <div key={s.label} style={{ background: '#f0fdf4', border: '1px solid #bbf7d0', padding: 16, borderRadius: 8 }}>
            <div style={{ fontWeight: 'bold', color: '#166534' }}>{s.label}</div>
            <div style={{ fontSize: 24, color: '#15803d' }}>{s.value.toLocaleString()} kgCO₂e</div>
          </div>
        ))}
      </div>

      <div style={{ background: '#f8fafc', border: '1px solid #e2e8f0', padding: 24, borderRadius: 8, marginBottom: 24 }}>
        <h2 style={{ marginTop: 0 }}>📤 Upload Data</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
          {[
            { type: 'SAP', label: '🏭 SAP Fuel/Procurement', color: '#dbeafe' },
            { type: 'UTILITY', label: '⚡ Utility Electricity', color: '#fef9c3' },
            { type: 'TRAVEL', label: '✈️ Corporate Travel', color: '#fce7f3' },
          ].map(s => (
            <div key={s.type} style={{ background: s.color, padding: 16, borderRadius: 8, textAlign: 'center' }}>
              <div style={{ fontWeight: 'bold', marginBottom: 8 }}>{s.label}</div>
              <input
                type="file"
                accept=".csv"
                onChange={(e) => handleUpload(e, s.type)}
                disabled={uploading}
                style={{ fontSize: 13 }}
              />
            </div>
          ))}
        </div>
        {message && (
          <div style={{ marginTop: 16, padding: 12, background: 'white', borderRadius: 8, border: '1px solid #e2e8f0' }}>
            {message}
          </div>
        )}
      </div>

      <div style={{ background: 'white', border: '1px solid #e2e8f0', borderRadius: 8, padding: 24 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <h2 style={{ margin: 0 }}>📋 Emission Records</h2>
          <div style={{ display: 'flex', gap: 8 }}>
            <select value={sourceFilter} onChange={e => setSourceFilter(e.target.value)}
              style={{ padding: '6px 12px', borderRadius: 6, border: '1px solid #e2e8f0' }}>
              <option value="">All Sources</option>
              <option value="SAP">SAP</option>
              <option value="UTILITY">Utility</option>
              <option value="TRAVEL">Travel</option>
            </select>
            <select value={statusFilter} onChange={e => setStatusFilter(e.target.value)}
              style={{ padding: '6px 12px', borderRadius: 6, border: '1px solid #e2e8f0' }}>
              <option value="">All Status</option>
              <option value="PENDING">Pending</option>
              <option value="APPROVED">Approved</option>
              <option value="FLAGGED">Flagged</option>
              <option value="REJECTED">Rejected</option>
            </select>
          </div>
        </div>

        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 14 }}>
          <thead>
            <tr style={{ background: '#f8fafc' }}>
              {['Source', 'Scope', 'Category', 'Raw Value', 'CO₂e (kg)', 'Period', 'Status', 'Flag', 'Actions'].map(h => (
                <th key={h} style={{ padding: '10px 12px', textAlign: 'left', borderBottom: '2px solid #e2e8f0' }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {records.length === 0 && (
              <tr><td colSpan={9} style={{ padding: 24, textAlign: 'center', color: '#9ca3af' }}>
                No records yet. Upload a CSV file above!
              </td></tr>
            )}
            {records.map(r => (
              <tr key={r.id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                <td style={{ padding: '10px 12px' }}><span style={{ background: '#dbeafe', padding: '2px 8px', borderRadius: 4, fontSize: 12 }}>{r.source_type}</span></td>
                <td style={{ padding: '10px 12px' }}>Scope {r.scope}</td>
                <td style={{ padding: '10px 12px' }}>{r.raw_category}</td>
                <td style={{ padding: '10px 12px' }}>{r.raw_value} {r.raw_unit}</td>
                <td style={{ padding: '10px 12px', fontWeight: 'bold' }}>{r.normalized_kgco2e?.toLocaleString()}</td>
                <td style={{ padding: '10px 12px', fontSize: 12 }}>{r.period_start}</td>
                <td style={{ padding: '10px 12px' }}>
                  <span style={{ background: statusColor(r.status), color: 'white', padding: '2px 8px', borderRadius: 4, fontSize: 12 }}>
                    {r.status}
                  </span>
                </td>
                <td style={{ padding: '10px 12px', fontSize: 12, color: '#f59e0b' }}>{r.flag_reason}</td>
                <td style={{ padding: '10px 12px' }}>
                  {!r.is_locked && (
                    <div style={{ display: 'flex', gap: 4 }}>
                      <button onClick={() => handleReview(r.id, 'APPROVED')}
                        style={{ background: '#22c55e', color: 'white', border: 'none', padding: '4px 8px', borderRadius: 4, cursor: 'pointer', fontSize: 12 }}>
                        ✓
                      </button>
                      <button onClick={() => handleReview(r.id, 'FLAGGED')}
                        style={{ background: '#f59e0b', color: 'white', border: 'none', padding: '4px 8px', borderRadius: 4, cursor: 'pointer', fontSize: 12 }}>
                        ⚑
                      </button>
                      <button onClick={() => handleReview(r.id, 'REJECTED')}
                        style={{ background: '#ef4444', color: 'white', border: 'none', padding: '4px 8px', borderRadius: 4, cursor: 'pointer', fontSize: 12 }}>
                        ✕
                      </button>
                    </div>
                  )}
                  {r.is_locked && <span style={{ color: '#9ca3af', fontSize: 12 }}>🔒 Locked</span>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
