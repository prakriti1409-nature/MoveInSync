// src/App.js
import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
} from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import FeedbackPage from "./pages/FeedbackPage";
import AdminDashboard from "./pages/AdminDashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import { clearToken, getToken } from "./api";
import "./App.css";

function Navbar() {
  const token = getToken();

  const handleLogout = () => {
    clearToken();
    window.location.href = "/login";
  };

  return (
    <header className="app-navbar">
      <div className="brand">Driver Sentiment Engine</div>
      <nav>
        {token && (
          <>
            <Link to="/feedback">Submit Feedback</Link>
            <Link to="/admin">Admin Dashboard</Link>
          </>
        )}
        {!token ? (
          <Link to="/login">Login</Link>
        ) : (
          <button onClick={handleLogout}>Logout</button>
        )}
      </nav>
    </header>
  );
}

function App() {
  return (
    <div className="app-root">
      <Router>
        <Navbar />
        <main className="app-content">
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/feedback"
              element={
                <ProtectedRoute>
                  <FeedbackPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin"
              element={
                <ProtectedRoute>
                  <AdminDashboard />
                </ProtectedRoute>
              }
            />
            <Route path="*" element={<LoginPage />} />
          </Routes>
        </main>
      </Router>
    </div>
  );
}

export default App;
