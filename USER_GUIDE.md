# FitNova – User & Developer Guide

Welcome to the FitNova User & Developer Guide. This document provides detail on running, testing, adding new features, troubleshooting, and production deployment checklists.

---

## 1. Running the Entire Project

### Step 1: Start the Postgres Database
Make sure PostgreSQL is running and you have created a database named `fitnova_db`.

### Step 2: Configure Environment Variables
Ensure your `backend/.env` is configured correctly:
```ini
DATABASE_URL=postgresql+psycopg2://postgres:2003@localhost:5432/fitnova_db
GROQ_API_KEY=gsk_***
SECRET_KEY=fitnova-secret-key
ENVIRONMENT=development
DEBUG=True
```

### Step 3: Run Database Migrations & Seeding
```bash
cd backend
source venv/bin/activate
alembic upgrade head
python scripts/seed.py
```

### Step 4: Run the Backend Service
```bash
uvicorn app.main:app --reload --port 8000
```
The API Swagger documentation will be available at `http://localhost:8000/docs`.

### Step 5: Run the Frontend React Application
Open a new terminal window:
```bash
cd frontend
npm run dev
```
Access the application dashboard at `http://localhost:5173`.

---

## 2. Sample Audio Files Required
FitNova's local transcription engine (Faster-Whisper) is configured to parse `.wav`, `.mp3`, and `.m4a` files.
- For testing purposes, you can upload any short audio recording (16kHz mono WAV format is highly recommended for faster transcription).
- A sample 14-byte dummy WAV is located at `backend/uploads/organization_1/dc93aeaa-d063-4bda-8566-839a0903037a.wav`.

---

## 3. Common Errors and Solutions

### Error 1: `ValueError: password cannot be longer than 72 bytes`
- **Cause**: Passlib compatibility check with python-bcrypt >= 4.0.0.
- **Solution**: Patched! We now use direct `bcrypt` calls to perform hashing and verification in `app/core/security.py`.

### Error 2: Database Connection Closed or Background Session Errors
- **Cause**: Reusing the FastAPI HTTP request database session in an asynchronous background task.
- **Solution**: Patched! The background tasks are enqueued using FastAPI `BackgroundTasks` with a dedicated `SessionLocal()` generator block which is closed immediately upon completion.

---

## 4. How to Add New Features

### 1. Adding a New Database Entity
1. Define the model class in `backend/app/models/` (e.g. `app/models/campaign.py`).
2. Register the model in `backend/app/models/__init__.py`.
3. Generate a database migration:
   ```bash
   alembic revision --autogenerate -m "Add campaign table"
   alembic upgrade head
   ```

### 2. Creating New API Endpoints
1. Create a schema in `backend/app/schemas/` defining the input and response structure.
2. Implement custom methods in `backend/app/crud/` if custom database queries are needed.
3. Expose endpoints in `backend/app/api/routers/` utilizing services and schemas.
4. Include the router in `backend/app/main.py`.

---

## 5. Production Readiness Checklist

- [ ] **Change default Secret Keys**: Replace `SECRET_KEY` in `.env` with a cryptographically secure key generated via `openssl rand -hex 32`.
- [ ] **Secure Database Connection**: Move the database url to secure AWS RDS or PGaaS instance using TLS/SSL connections.
- [ ] **Disable Swagger in Production**: Set `DEBUG=False` and configure FastAPI to hide `/docs` on production environments.
- [ ] **Compute Hardware for Whisper**: In production, configure `device="cuda"` in `FasterWhisper` initialization if running on a GPU-enabled server to speed up transcription by up to 10x.
- [ ] **CORS Settings**: Update `allow_origins` in `app/main.py` to match the exact production domain of your dashboard instead of wildcard/localhost.
- [ ] **Vite Production Bundles**: Run `npm run build` on Vite frontend and serve static files using Nginx or CDN (Cloudflare/Vercel).
