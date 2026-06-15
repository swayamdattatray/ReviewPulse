import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../api';

export default function Dashboard() {
  const { user } = useAuth();
  const [health, setHealth] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    api.health()
      .then(setHealth)
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <p>Welcome back, {user?.first_name || user?.username}</p>
      </div>

      <div className="cards">
        <div className="card">
          <div className="card-icon green">&#10003;</div>
          <div className="card-info">
            <h3>API Status</h3>
            <p>{health?.status || 'Checking...'}</p>
          </div>
        </div>
        <div className="card">
          <div className="card-icon blue">v</div>
          <div className="card-info">
            <h3>API Version</h3>
            <p>{health?.version || '—'}</p>
          </div>
        </div>
        <div className="card">
          <div className="card-icon purple">@</div>
          <div className="card-info">
            <h3>Your Role</h3>
            <p>{user?.role || '—'}</p>
          </div>
        </div>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {health && (
        <div className="section">
          <h2>Available Endpoints</h2>
          <div className="endpoint-grid">
            {Object.entries(health.endpoints).map(([key, value]) => (
              <div key={key} className="endpoint-card">
                <h4>{key.replace(/_/g, ' ')}</h4>
                {typeof value === 'string' ? (
                  <code>{value}</code>
                ) : (
                  <ul>
                    {Object.entries(value).map(([k, v]) => (
                      <li key={k}>
                        <strong>{k}:</strong> <code>{v}</code>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="section">
        <h2>Profile</h2>
        <div className="profile-card">
          <table>
            <tbody>
              <tr><td>Username</td><td>{user?.username}</td></tr>
              <tr><td>Email</td><td>{user?.email}</td></tr>
              <tr><td>Name</td><td>{user?.first_name} {user?.last_name}</td></tr>
              <tr><td>Role</td><td>{user?.role}</td></tr>
              <tr><td>Member since</td><td>{user?.created_at ? new Date(user.created_at).toLocaleDateString() : '—'}</td></tr>
              <tr><td>Last login</td><td>{user?.last_login ? new Date(user.last_login).toLocaleString() : '—'}</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
