# IoT AI Calorie Tracker

## Overview
An IoT-based calorie tracking system using ESP32-CAM, FastAPI, PostgreSQL, and Google Gemini Vision API.

The system captures food images, identifies the food using AI, calculates calories based on weight, and logs consumption for analytics.

---

## Tech Stack

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy
- Google Gemini API (Vision + Nutrition)
- Python

### Hardware (Planned Integration)
- ESP32-CAM
- Load Cell (HX711)
- WiFi Module

---

## Architecture

ESP32-CAM  
↓  
FastAPI Backend  
↓  
Gemini Vision API (Food Identification)  
↓  
PostgreSQL (Nutrition Database)  
↓  
Calorie Calculation  
↓  
Logs & Analytics APIs  

---

## Features Implemented

### Phase 0 – Project Setup 
- Backend folder structure
- Database configuration
- GitHub integration
- API documentation (Swagger)

### Phase 1 – Backend Core System 
- User & Device management
- Food database schema
- Calorie calculation service
- Log storage
- Daily calorie tracking
- Weekly analytics API

### Phase 2 – AI Integration (Gemini) 
- Image upload endpoint
- Gemini Vision-based food recognition
- Dynamic nutrition generation
- Automatic food insertion into database
- Removal of local ML models (TensorFlow removed)
- Clean AI-powered architecture

System now supports:
- Automatic learning of new foods
- No manual dataset maintenance
- Fully dynamic nutrition database

---

## Current System Flow

1. User places food on load cell.
2. ESP32 captures image.
3. Backend sends image to Gemini.
4. Gemini returns food name.
5. If food not in database → nutrition auto-generated.
6. Calories calculated using weight.
7. Entry stored in logs.
8. Analytics available via API.

---

## Remaining Work (Phase 3 – IoT Integration)

- ESP32-CAM firmware setup
- Capture and send image via HTTP POST
- Integrate load cell for automatic weight capture
- End-to-end real hardware testing
- Error handling & retry logic
- Production hardening

---

## Future Enhancements

- Portion estimation using AI
- Structured JSON responses from Gemini
- Frontend dashboard (React)
- User authentication (JWT)
- Deployment to cloud (AWS / GCP)
- Caching Gemini responses
- Nutrition validation layer

---

## Project Status

Phase 0 – Complete  
Phase 1 – Complete  
Phase 2 – Complete (Gemini AI Integrated)  
Phase 3 – In Progress (ESP32 Hardware Integration)
