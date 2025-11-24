// src/api.js
const API_BASE_URL = "http://127.0.0.1:8000/api";

export function getToken() {
  return localStorage.getItem("authToken");
}

export function setToken(token) {
  localStorage.setItem("authToken", token);
}

export function clearToken() {
  localStorage.removeItem("authToken");
}

async function request(path, options = {}) {
  const token = getToken();

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (token) {
    headers["Authorization"] = `Token ${token}`;
  }

  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  const data = await res.json().catch(() => null);

  if (!res.ok) {
    const message = data?.detail || data?.message || "Request failed";
    throw new Error(message);
  }

  return data;
}

export function login(username, password) {
  return request("/auth/token/", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

export function submitFeedback(payload) {
  return request("/feedback/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function fetchFeedbackConfig() {
  return request("/config/feedback-types/");
}

export function fetchDriverSentiments() {
  return request("/drivers/sentiments/");
}

export function fetchAlerts() {
  return request("/alerts/");
}
