// src/pages/FeedbackPage.js
import React, { useEffect, useState } from "react";
import { submitFeedback, fetchFeedbackConfig } from "../api";

export default function FeedbackPage() {
  const [config, setConfig] = useState([]);
  const [loadingConfig, setLoadingConfig] = useState(true);
  const [form, setForm] = useState({
    entity_type: "DRIVER",
    driver_id: "",
    trip_id: "",
    rating: "",
    text: "",
  });
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    async function loadConfig() {
      try {
        const data = await fetchFeedbackConfig();
        setConfig(data);
      } catch (err) {
        console.error("Failed to load feedback config:", err);
      } finally {
        setLoadingConfig(false);
      }
    }
    loadConfig();
  }, []);

  const isEnabled = (key) => {
    const item = config.find((c) => c.key === key);
    return item ? item.enabled : true;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name === "entity_type") {
      setForm((prev) => ({
        ...prev,
        entity_type: value,
        driver_id: "",
        trip_id: "",
      }));
      setMessage("");
      return;
    }

    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setMessage("");

    try {
      const payload = {
        entity_type: form.entity_type,
        driver:
          form.entity_type === "DRIVER" && form.driver_id
            ? form.driver_id // employee_id string like DR001
            : null,
        trip:
          form.entity_type === "TRIP" && form.trip_id
            ? Number(form.trip_id)
            : null,
        rating: form.rating ? Number(form.rating) : null,
        text: form.text,
      };

      await submitFeedback(payload);
      setMessage("Feedback submitted successfully!");

      setForm((prev) => ({
        ...prev,
        rating: "",
        text: "",
      }));
    } catch (err) {
      setMessage(err.message || "Failed to submit feedback");
    } finally {
      setSubmitting(false);
    }
  };

  if (loadingConfig) return <p>Loading...</p>;

  const entityOptions = [];
  if (isEnabled("driver"))
    entityOptions.push({ value: "DRIVER", label: "Driver" });
  if (isEnabled("trip")) entityOptions.push({ value: "TRIP", label: "Trip" });
  if (isEnabled("app"))
    entityOptions.push({ value: "APP", label: "Mobile App" });
  if (isEnabled("marshal"))
    entityOptions.push({ value: "MARSHAL", label: "Marshal" });

  return (
    <div className="page-card">
      <h2 className="page-title">Submit Feedback</h2>
      <p className="page-subtitle">
        Share your experience so we can proactively monitor driver sentiment.
      </p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">Entity Type</label>
          <select
            name="entity_type"
            value={form.entity_type}
            onChange={handleChange}
            className="form-select"
          >
            {entityOptions.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>

        {form.entity_type === "DRIVER" && (
          <div className="form-group">
            <label className="form-label">Driver ID (code)</label>
            <input
              type="text"
              name="driver_id"
              value={form.driver_id}
              onChange={handleChange}
              className="form-input"
              placeholder="e.g. DR001"
              required
            />
          </div>
        )}

        {form.entity_type === "TRIP" && (
          <div className="form-group">
            <label className="form-label">Trip ID</label>
            <input
              type="number"
              name="trip_id"
              value={form.trip_id}
              onChange={handleChange}
              className="form-input"
              placeholder="Enter Trip ID"
            />
          </div>
        )}

        <div className="form-group">
          <label className="form-label">Rating (1–5)</label>
          <input
            type="number"
            name="rating"
            min="1"
            max="5"
            value={form.rating}
            onChange={handleChange}
            className="form-input"
            placeholder="Optional numeric rating"
          />
        </div>

        <div className="form-group">
          <label className="form-label">Feedback Text</label>
          <textarea
            name="text"
            value={form.text}
            onChange={handleChange}
            className="form-textarea"
            required
          />
        </div>

        {message && (
          <p
            className={`msg ${
              message.includes("successfully") ? "msg-success" : "msg-error"
            }`}
          >
            {message}
          </p>
        )}

        <button type="submit" className="btn-primary" disabled={submitting}>
          {submitting ? "Submitting..." : "Submit Feedback"}
        </button>
      </form>
    </div>
  );
}
