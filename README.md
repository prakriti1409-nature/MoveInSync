
# MoveInSync – Driver Sentiment Engine

A real-time Driver Sentiment Engine designed to analyze rider feedback, classify sentiment, track driver performance, and generate proactive alerts for risky drivers. This project fulfills the official MoveInSync case study requirements using Django REST Framework, React, and SQLite.

## 🚀 Features

### 🔐 Authentication
- Secure login using DRF Token Authentication
- All APIs except login require authentication

### 📝 Feedback Collection
Supports feedback for:
- Driver
- Trip
- Mobile App Experience
- Marshal (on-ground staff)

All feedback types are feature-flag configurable via admin panel.

### 🧠 Sentiment Analysis Engine
- Lightweight rule-based NLP engine
- Classifies sentiment as Positive / Neutral / Negative
- Assigns a score (1–5)
- Handles typos, emojis, slang via keyword mapping

### 📊 Real-Time Driver Sentiment Summary
- Rolling average sentiment (O(1))
- Total feedback count
- Last feedback timestamp

### 🚨 Risk Alerts
Alerts automatically generated when:
- Driver average score < threshold (default: 2.5)
- AND no existing OPEN alert

### 🎛 Admin Dashboard
Includes:
- Driver sentiment tables
- Alerts list
- Bar chart visualization
- Responsive UI

## 🏗 Architecture Overview
frontend/ → React  
backend/  
  ├── core/ → Feedback engine, alerts, APIs  
  ├── sentiment/ → Rule-based engine  
  ├── db.sqlite3 → SQLite Database  

## 📡 API Endpoints
POST /api/auth/token/  
POST /api/feedback/  
GET /api/config/feedback-types/  
GET /api/drivers/sentiments/  
GET /api/alerts/  

## 🧩 Setup Instructions
Clone repo → Set up backend → Set up frontend → Run servers.

## 🧠 Core Algorithms
Rolling Average (O(1))  
Alert Logic  
Sentiment Classification Basics  

## ❗ Limitations
- Rule-based sentiment is basic  
- SQLite not scalable  
- No async or ML yet



