// src/pages/AdminDashboard.js
import React, { useEffect, useState } from "react";
import { fetchDriverSentiments, fetchAlerts } from "../api";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

export default function AdminDashboard() {
  const [driverSentiments, setDriverSentiments] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        const [sentimentsData, alertsData] = await Promise.all([
          fetchDriverSentiments(),
          fetchAlerts(),
        ]);
        setDriverSentiments(sentimentsData);
        setAlerts(alertsData);
      } catch (err) {
        console.error(err);
        setError(err.message || "Failed to load dashboard");
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) return <p>Loading dashboard...</p>;

  // Prepare data for bar chart
  const chartData = driverSentiments.map((item) => ({
    name: item.driver.employee_id || item.driver.name,
    avgScore: item.avg_score,
  }));

  return (
    <div className="page-card">
      <h2 className="page-title">Admin Dashboard</h2>
      <p className="page-subtitle">
        Monitor driver sentiment trends and identify risky drivers in real time.
      </p>

      {error && <p className="msg msg-error">{error}</p>}

      {/* --- Chart Section --- */}
      <section>
        <h3 className="section-title">Driver Sentiment Overview</h3>
        {chartData.length === 0 ? (
          <p className="msg">No sentiment data available yet.</p>
        ) : (
          <div style={{ width: "100%", height: 260 }}>
            <ResponsiveContainer>
              <BarChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 30 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="name"
                  angle={-25}
                  textAnchor="end"
                  height={60}
                />
                <YAxis domain={[0, 5]} />
                <Tooltip />
                <Bar dataKey="avgScore" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </section>

      {/* --- Table: Driver Sentiment Summary --- */}
      <section>
        <h3 className="section-title">Driver Sentiment Summary</h3>
        <div className="table-wrapper">
          <table className="table">
            <thead>
              <tr>
                <th>Driver ID</th>
                <th>Driver Name</th>
                <th>Employee ID</th>
                <th>Avg Score</th>
                <th>Total Feedback</th>
                <th>Last Feedback At</th>
              </tr>
            </thead>
            <tbody>
              {driverSentiments.length === 0 ? (
                <tr>
                  <td colSpan="6">No sentiment data available yet.</td>
                </tr>
              ) : (
                driverSentiments.map((item) => (
                  <tr key={item.driver.id}>
                    <td>{item.driver.id}</td>
                    <td>{item.driver.name}</td>
                    <td>{item.driver.employee_id}</td>
                    <td>{item.avg_score.toFixed(2)}</td>
                    <td>{item.total_feedback_count}</td>
                    <td>{item.last_feedback_at}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>

      {/* --- Table: Alerts --- */}
      <section>
        <h3 className="section-title">Alerts</h3>
        {alerts.length === 0 ? (
          <p className="msg">No alerts</p>
        ) : (
          <div className="table-wrapper">
            <table className="table">
              <thead>
                <tr>
                  <th>Driver</th>
                  <th>Avg Score at Alert</th>
                  <th>Threshold</th>
                  <th>Status</th>
                  <th>Created At</th>
                </tr>
              </thead>
              <tbody>
                {alerts.map((alert) => (
                  <tr key={alert.id}>
                    <td>
                      {alert.driver.name} ({alert.driver.employee_id})
                    </td>
                    <td>{alert.avg_score_at_creation.toFixed(2)}</td>
                    <td>{alert.threshold}</td>
                    <td>{alert.status}</td>
                    <td>{alert.created_at}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}
