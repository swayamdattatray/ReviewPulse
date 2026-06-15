import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path ? 'active' : '';

  return (
    <nav className="navbar">
      <Link to="/" className="nav-brand">ReviewIQ</Link>
      <div className="nav-links">
        {user ? (
          <>
            <Link to="/dashboard" className={isActive('/dashboard')}>Dashboard</Link>
            <Link to="/products" className={isActive('/products')}>Products</Link>
            <Link to="/reviews" className={isActive('/reviews')}>Reviews</Link>
            <Link to="/analytics" className={isActive('/analytics')}>Analytics</Link>
            <Link to="/trends" className={isActive('/trends')}>Trends</Link>
            <span className="nav-divider" />
            <span className="nav-user">{user.username}</span>
            <button onClick={handleLogout} className="btn btn-sm">Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register" className="btn btn-primary btn-sm">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}
