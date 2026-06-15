import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Products from './pages/Products';
import ProductDetail from './pages/ProductDetail';
import Reviews from './pages/Reviews';
import Analytics from './pages/Analytics';
import Trends from './pages/Trends';
import './App.css';

function PrivateRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="loading">Loading...</div>;
  return user ? children : <Navigate to="/login" />;
}

function PublicRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="loading">Loading...</div>;
  return user ? <Navigate to="/dashboard" /> : children;
}

function Home() {
  const { user } = useAuth();
  return (
    <div className="home-page">
      <div className="hero">
        <h1>ReviewIQ</h1>
        <p>AI-Powered Customer Review Intelligence Platform</p>
        <div className="hero-features">
          <span>Sentiment Analysis</span>
          <span>Fake Review Detection</span>
          <span>AI Content Detection</span>
          <span>Smart Recommendations</span>
          <span>Trend Forecasting</span>
        </div>
        <div className="hero-actions">
          {user ? (
            <a href="/dashboard" className="btn btn-primary">Go to Dashboard</a>
          ) : (
            <>
              <a href="/register" className="btn btn-primary">Get Started</a>
              <a href="/login" className="btn">Sign In</a>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Navbar />
        <main className="container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
            <Route path="/register" element={<PublicRoute><Register /></PublicRoute>} />
            <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
            <Route path="/products" element={<PrivateRoute><Products /></PrivateRoute>} />
            <Route path="/products/:id" element={<PrivateRoute><ProductDetail /></PrivateRoute>} />
            <Route path="/reviews" element={<PrivateRoute><Reviews /></PrivateRoute>} />
            <Route path="/analytics" element={<PrivateRoute><Analytics /></PrivateRoute>} />
            <Route path="/trends" element={<PrivateRoute><Trends /></PrivateRoute>} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </main>
      </AuthProvider>
    </BrowserRouter>
  );
}
