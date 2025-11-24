
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

### 🧠 ML-Powered Sentiment Analysis (VADER) <OPTIONAL>
 Fully integrated VADER sentiment analysis model:
- Produces compound sentiment score
- Maps score → 1–5 rating
- Categorizes sentiment → Positive / Neutral / Negative
- Robust to typos, emojis, slang, long text
- Pluggable Sentiment Engine Design
 You can easily swap VADER with:
- Hugging Face transformers
- BERT-based models
- Remote ML microservice
without changing any API or database structure.

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

## now some screenshots :
<img width="1914" height="469" alt="image" src="https://github.com/user-attachments/assets/7785d07a-6c06-46a2-ac31-dffd1f5a4255" />
<img width="1903" height="643" alt="image" src="https://github.com/user-attachments/assets/a1b92be7-5c37-4509-8bb9-fb66971ee6f7" />
<img width="989" height="570" alt="image" src="https://github.com/user-attachments/assets/0463eebc-6fb9-45a7-a166-81e171029f90" />
<img width="933" height="597" alt="image" src="https://github.com/user-attachments/assets/8fafb111-f8ef-4c63-8d59-2d20a7b39efc" />
<img width="956" height="730" alt="image" src="https://github.com/user-attachments/assets/65d9584d-86e7-4584-88ca-d3d71a7ec54f" />


