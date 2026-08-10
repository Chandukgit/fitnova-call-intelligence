# FitNova – AI Call Intelligence Platform

FitNova is an enterprise-grade AI-powered Call Intelligence Platform that processes customer support and sales audio recordings. It provides automated Whisper transcription, Groq LLM-driven conversations analysis, advisor scorecard grading, sentiment analysis, structured issue tagging, and a React analytics dashboard.

---

## 1. Project Overview

FitNova helps customer support and sales teams analyze call recordings to evaluate advisor performance, track customer sentiment, tag critical compliance/product issues, and provide actionable recommendations.

```mermaid
graph TD
    A[Customer uploads audio] --> B[FastAPI Backend saves audio]
    B --> C[Background task enqueued]
    C --> D[Faster-Whisper transcribes audio]
    D --> E[Prompt Builder constructs LLM prompt]
    E --> F[Groq LLM Llama-3.3 analyzes transcript]
    F --> G[Parse JSON result & structured issue tags]
    G --> H[Store Summary, Score, Tags in PostgreSQL]
    H --> I[React Dashboard displays updated analytics]
```

---

## 2. Folder Structure

```
fitnova/
├── backend/
│   ├── alembic/                # DB Migrations folder
│   ├── app/
│   │   ├── ai/                 # AI Engines (Whisper, Groq)
│   │   │   ├── analysis/       # Processing Pipeline & Orchestrator
│   │   │   ├── llm/            # Groq Wrapper & Config
│   │   │   └── prompts/        # Analysis prompts & templates
│   │   ├── api/                # API Routers & Dependencies
│   │   ├── core/               # App config, auth helpers, exception handlers
│   │   ├── database/           # DB sessions & Base model setup
│   │   ├── models/             # SQLAlchemy 2.0 Models
│   │   ├── schemas/            # Pydantic Schemas
│   │   ├── services/           # Business logic layer
│   │   └── storage/            # Local storage helper
│   ├── scripts/                # Database seeding & test scripts
│   ├── .env                    # Backend environment config
│   └── requirements.txt        # Backend dependencies
└── frontend/
    ├── src/
    │   ├── components/         # Reusable UI Components
    │   ├── pages/              # Pages (Dashboard, CallDetails, Upload, Login)
    │   ├── services/           # API Client & Services
    │   └── App.css             # Main styling
    ├── package.json            # Node modules & scripts
    └── vite.config.js          # Vite config
```

---

## 3. Technologies Used

### Backend
- **FastAPI**: Modern, high-performance web framework.
- **SQLAlchemy 2.0**: Object-relational mapping.
- **PostgreSQL**: Production-grade relational database.
- **JWT & Bcrypt**: Robust authentication & password hashing.
- **Faster-Whisper**: High-speed, local transcription using Whisper models.
- **Groq Llama-3.3-70b**: Ultra-fast LLM API for analysis.
- **Alembic**: Database schema migrations.

### Frontend
- **React (Vite)**: Rapid and modern UI development.
- **Axios**: API client.
- **Recharts & Lucide React**: Dashboard visualizations & modern icons.
- **Framer Motion**: Smooth micro-animations.
- **TailwindCSS**: CSS styling utility.

---

## 4. Architecture Explanation

FitNova uses a decoupled **n-tier architecture**:
1. **Presentation Layer**: A single page React application compiled via Vite communicating over JSON REST API.
2. **Controller/Routing Layer (FastAPI)**: Exposes endpoints protected by JWT OAuth2 authentication.
3. **Service Layer**: Decoupled business logic separating controllers from direct database CRUD operations.
4. **Data Access Layer (SQLAlchemy 2.0)**: Generic repository pattern (`CRUDBase`) mapping models dynamically.
5. **AI Pipeline Orchestrator**: Runs CPU/IO intensive tasks in background workers using FastAPI's background tasks to avoid blocking web requests.

---

## 5. Database Schema

The relational database schema is structured as follows:

```
Organizations (1) ── (N) Teams
                       │
                       └── (N) Advisors (1) ── (N) Calls ── (1) Transcripts
                                                     │
                                                     └── (1) Analyses ── (N) IssueTags
```

- **Organizations**: Company metadata.
- **Teams**: Sales/support departments.
- **Advisors**: Customer support representatives.
- **Customers**: Caller profiles.
- **Calls**: Log of uploaded calls, audio metadata, language, and transcription/analysis statuses.
- **Transcripts**: Full text transcription and word count mapping.
- **Analyses**: Advisor performance grades (Discovery, Objection, Compliance, closing subscores), overall scores, and LLM summary text.
- **IssueTags**: Flagged points of friction with timestamp, quoted text, severity, and reason.

---

## 6. Authentication Flow

```
1. Client POSTs credentials -> /auth/login
2. Backend queries user by email & verifies password using bcrypt
3. Backend returns JWT Access Token (HS256 signature, 1 hour expiration)
4. Client stores JWT in localStorage / sessionStorage
5. Client attaches "Authorization: Bearer <token>" on subsequent API requests
6. Backend intercepts & validates token using jose, extracting user claims
```

---

## 7. AI Pipeline Explanation

```
1. Client uploads WAV/MP3 -> /upload/audio
2. Backend generates unique UUID file path, writes bytes locally to "backend/uploads"
3. Call record is created in "UPLOADED" status
4. Background task triggers "analysis_pipeline.process"
5. Call status changes to "TRANSCRIBING" -> Faster-Whisper transcribes audio to text
6. Call status changes to "ANALYZING" -> Text is structured into Prompt Template
7. Prompt is sent to Groq Llama-3.3-70b-versatile, which responds with structured JSON
8. Analysis record and structured Issue Tags are parsed and saved to the DB
9. Call status changes to "COMPLETED"
```

---

## 8. Installation Guide

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL server

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example` (or edit existing `.env`):
   ```ini
   DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/fitnova_db
   GROQ_API_KEY=YOUR_GROQ_API_KEY
   SECRET_KEY=YOUR_SECRET_JWT_KEY
   DEBUG=True
   ```
5. Apply database migrations:
   ```bash
   alembic upgrade head
   ```
6. Seed database with initial data:
   ```bash
   python scripts/seed.py
   ```
7. Start the backend:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install packages:
   ```bash
   npm install
   ```
3. Start frontend dev server:
   ```bash
   npm run dev
   ```

---

## 9. Login Credentials

Seed data creates three users with different role permissions:
- **Admin Role**: `admin@fitnova.ai` / Password: `Admin@123`
- **Manager Role**: `manager@fitnova.ai` / Password: `Manager@123`
- **Advisor Role**: `john.carter@fitnova.ai` / Password: `Advisor@123`

---

## 10. Sample Test Flow

1. Log in to the React Dashboard as `admin@fitnova.ai`.
2. Go to **Upload call recording**.
3. Select Advisor (e.g. John Carter), Customer (e.g. Alex Brown), and select a `.wav` or `.mp3` file.
4. Click **Upload audio**.
5. Once the upload finishes, navigate back to **Calls**. You will see the new call processing through `TRANSCRIBING` and `ANALYZING`.
6. Once marked `COMPLETED`, click on the Call to see the transcript text, quality score, recommendations, and structured issue tags highlighted in real-time.
