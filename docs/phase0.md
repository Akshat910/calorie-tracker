Microcontroller: ESP32
Backend: FastAPI (Python)
Database: PostgreSQL
Frontend: React (optional for MVP)
Protocol: HTTP REST

Dataflow:
1. ESP32 measures weight
2. ESP32 captures image
3. Sends both to backend
4. Backend predicts food
5. Backend calculates calories
6. Backend stores log
7. Frontend displays result