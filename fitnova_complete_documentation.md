# FitNova Call Intelligence Platform: Complete Reference & Interview Guide

This document is a comprehensive technical specification, architectural review, and implementation guide for the FitNova Call Intelligence Platform. It details the technologies, architecture, security schemas, RAG pipeline, and RAG evaluation metrics designed and implemented in the system.

---

## 1. System Architecture Overview

FitNova is designed using a decoupled, highly responsive **n-tier architecture**. The system separates concern levels to optimize horizontal scaling, security, and computational efficiency for AI workloads (transcription and LLM analysis).

### Architectural Diagram
```
                     +---------------------------------------+
                     |         React Frontend (Vite)         |
                     |  (Framer Motion, Tailwind, Recharts)  |
                     +---------------------------------------+
                                         |
                                         | JWT Auth Header / HTTP REST API
                                         v
                     +---------------------------------------+
                     |            FastAPI Backend            |
                     |  - APIRouters (Auth, Calls, RAG, etc) |
                     |  - CORS & Exception Handlers          |
                     +---------------------------------------+
                       /                 |                 \
  DB Query            /                  |                  \ Asynchronous Task
  SQLAlchemy         v                   |                   v
+------------------------+               |               +-------------------------+
| PostgreSQL + pgvector  |               |               | Local Audio Storage     |
| - Users, Call Metadata |               |               | (/uploads)              |
| - Document Vectors     |               |               +-------------------------+
+------------------------+               |                            |
                                         v                            | Read WAV/MP3
                     +---------------------------------------+        |
                     |          AI Engine Pipeline           |<-------+
                     | - Faster-Whisper (Local CPU/Int8)     |
                     | - Docling Document Parser             |
                     | - Groq LLM API (Qwen/LLaMA JSON mode) |
                     +---------------------------------------+
```

### Layer Breakdown
1. **Presentation Layer (React/Vite)**: An optimized Single-Page Application (SPA) utilizing Framer Motion for micro-animations and Recharts for call performance analytics.
2. **Controller/Routing Layer (FastAPI)**: Routes requests to specific business controllers. Employs security dependencies for role checks and handles request validations using Pydantic.
3. **Service Layer**: Decoupled modules containing core operations (e.g., call analysis, document ingestion).
4. **Data Access Layer (SQLAlchemy 2.0)**: Coordinates communication with PostgreSQL.
5. **AI Pipeline Orchestrator**: Executes heavy AI processes (Whisper, Groq) as asynchronous background tasks.

---

## 2. REST API & Endpoint Implementation

FitNova enforces standard REST conventions: nouns as resources, appropriate HTTP methods, status codes, and Pydantic-validated request/response bodies.

### Detailed Endpoint Example: `/knowledge/chat`
This endpoint allows users to chat with uploaded documents using context retrieved via semantic vector search.

#### Pydantic Schemas (`app/schemas/knowledge.py`)
```python
from pydantic import BaseModel, Field
from typing import List

class ChatRequest(BaseModel):
    question: str = Field(..., description="The query to ask the knowledge base")

class SourceCitation(BaseModel):
    file_name: str
    heading: str
    chunk_index: int

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceCitation]
```

#### API Controller Route (`app/api/routers/knowledge.py`)
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.knowledge import ChatRequest, ChatResponse, SourceCitation
from app.services.knowledge import knowledge_service
from app.ai.llm.groq_provider import groq_provider

router = APIRouter(prefix="/knowledge", tags=["Knowledge Base"])

def get_user_org_id(user: User) -> int:
    if not user.advisor or not user.advisor.team:
        return 1  # Admin/Fallback Organization ID
    return user.advisor.team.organization_id

@router.post("/chat", response_model=ChatResponse)
def chat_with_knowledge(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    org_id = get_user_org_id(current_user)
    
    # 1. Retrieve matching chunks via Semantic Search (SQLAlchemy pgvector)
    similar_chunks = knowledge_service.search_similar_chunks(
        db=db, query=request.question, organization_id=org_id, top_k=5
    )

    if not similar_chunks:
        return ChatResponse(
            answer="I couldn't find any documents related to your query in the Knowledge Base.",
            sources=[]
        )

    # 2. Compile context string
    context_blocks = []
    for chunk in similar_chunks:
        context_blocks.append(f"Source: {chunk['file_name']} | Section: {chunk['heading']}\nContent: {chunk['content']}")
    context_str = "\n\n---\n\n".join(context_blocks)

    # 3. Raise API prompt to Groq LLM
    prompt = f"""You are a FitNova Knowledge Assistant. You help users answer questions based strictly on internal organization documents.
Answer the user's question using ONLY the provided document context. If the answer cannot be found in the context, say "I cannot find the answer in the provided documents."

Return your response as a JSON object with a single key "answer" containing your grounded response.

Context:
{context_str}

Question:
{request.question}
"""
    try:
        llm_response = groq_provider.generate(prompt)
        answer = llm_response.get("answer", "No answer could be generated.")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating response from LLM: {str(e)}"
        )

    # 4. Compile Citations
    sources = []
    seen = set()
    for chunk in similar_chunks:
        source_key = (chunk["file_name"], chunk["heading"])
        if source_key not in seen:
            seen.add(source_key)
            sources.append(SourceCitation(
                file_name=chunk["file_name"],
                heading=chunk["heading"],
                chunk_index=chunk["chunk_index"]
            ))

    return ChatResponse(answer=answer, sources=sources)
```

### Other Main Endpoint Declarations
Below are key route definitions used to orchestrate the platform:
- **Calls Route (`/calls`)**:
  - `POST /calls/upload`: Uploads WAV/MP3, registers the Call record in DB, and spawns the background transcription/analysis task.
  - `GET /calls/{id}`: Returns full call transcript, analysis metrics, sentiment, and compliance tags.
  - `GET /calls`: Paginated call list with filters for Advisor and Customer.
- **Feedback Route (`/feedback`)**:
  - `POST /feedback`: Creates manager feedback on graded scorecards.
- **Advisor Route (`/advisors`)**:
  - `GET /advisors/scorecard`: Aggregated metrics for performance (Objection handling, compliance).

---

## 3. JWT Authentication & Role-Based Authorization

FitNova implements token-based authentication using **JSON Web Tokens (JWT)** with `HS256` signature algorithm. 

### Encryption & Password Salting (`app/core/security.py`)
Plaintext passwords are never stored. We use `bcrypt` to generate salts and execute verification:
```python
import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.core.config import settings

def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except Exception:
        return False
```

### Token Creation & Verification (`app/core/security.py` & `auth.py`)
When a user logs in via POST request to `/auth/login`, we generate an access token:
```python
def create_access_token(subject: str, expires_delta: timedelta = None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(hours=1))
    payload = {"sub": str(subject), "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
```
Every secure endpoint injects `get_current_user` as a FastAPI Dependency:
```python
# app/core/auth.py
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except Exception:
        raise UnauthorizedException("Invalid authentication credentials.")
        
    db_user = user.get(db, user_id)
    if db_user is None or not db_user.is_active:
        raise UnauthorizedException("User inactive or not found.")
    return db_user
```

### Role-Based Access Control (RBAC) (`app/core/permissions.py`)
FitNova enforces strict role controls: **Admin**, **Manager**, and **Advisor**.
```python
# app/core/permissions.py
from fastapi import Depends
from app.core.auth import get_current_user
from app.core.enums import UserRole
from app.core.exceptions import ForbiddenException

def require_roles(*roles: UserRole):
    def checker(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            raise ForbiddenException("You do not have permission to perform this action.")
        return current_user
    return checker
```
**Endpoint Usage Example:**
```python
@router.post("/users", dependencies=[Depends(require_roles(UserRole.ADMIN))])
def create_new_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # Only authenticated admin accounts can reach this logic block
    return user_service.create(db, obj_in=user_in)
```

---

## 4. SQLAlchemy 2.0 ORM & Database Layer

FitNova uses **SQLAlchemy 2.0** ORM to manage Postgres relations. 

### Why SQLAlchemy 2.0?
1. **Type-Safety (`Mapped` / `mapped_column`)**: Fully compatible with Python typing checkers like mypy, eliminating run-time mapping bugs.
2. **Explicit Query Style**: Unified query executions using standard `select()`, `insert()`, `update()`, and `delete()` constructs instead of implicit `session.query(Model)`.
3. **Engine-Level Performance**: Built-in support for asynchronous run loops and efficient connection pooling.

### Core Database Model Relationship Definition
```python
from sqlalchemy import ForeignKey, Enum, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    
    # 1-to-N with Teams
    teams: Mapped[list["Team"]] = relationship(back_populates="organization", cascade="all, delete-orphan")

class Team(Base):
    __tablename__ = "teams"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    
    organization: Mapped[Organization] = relationship(back_populates="teams")
    advisors: Mapped[list["Advisor"]] = relationship(back_populates="team")
```

---

## 5. Audio Transcription: Faster-Whisper

### What is Faster-Whisper?
**Faster-Whisper** is a re-implementation of OpenAI's Whisper model using **CTranslate2**, a fast inference engine for Transformer models. It achieves **4x to 10x higher execution speeds** compared to OpenAI's native implementation, requiring significantly less memory.

### Why We Used It locally on CPU
- **Data Privacy / Security**: Audio containing sales details or client PII does not leave local servers.
- **Cost**: No external API fees (e.g. OpenAI transcription APIs charge $0.006 per minute).
- **Quantization Optimization**: We configured `compute_type="int8"`, converting model weights from float32/float16 to 8-bit integers. This allows local CPU execution with negligible loss in accuracy.

### Core Transcription Code (`app/ai/whisper/faster_whisper.py`)
```python
from faster_whisper import WhisperModel
from app.ai.whisper.base import WhisperBase

class FasterWhisper(WhisperBase):
    def __init__(self):
        # Initialize Whisper Model on CPU utilizing Int8 quantization
        self.model = WhisperModel(
            model_size_or_path="base",
            device="cpu",
            compute_type="int8",
        )

    def transcribe(self, audio_path: str) -> dict:
        # Segment iterator yields timestamped transcribed segments
        segments, info = self.model.transcribe(audio_path)
        
        transcript = []
        full_text = ""

        for segment in segments:
            transcript.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip(),
            })
            full_text += segment.text + " "

        return {
            "text": full_text.strip(),
            "language": info.language,
            "language_probability": info.language_probability,
            "segments": transcript,
        }
```

---

## 6. Document Ingestion & Chunking via Docling

### What is Docling?
**Docling** is a structured document conversion parser. It parses heterogeneous document formats (PDFs, Docx, HTML) and outputs detailed, hierarchy-aware representations.

### Why Docling Over Standard Text Parsers?
Standard text parsers (like PyPDF2) strip text indiscriminately, destroying structures like headers, markdown formatting, lists, and tables. If a heading is split away from its body text, vector embeddings lose the context of *what* that paragraph is about. Docling exports structured markdown layouts, enabling **section-aware structural splitting**.

### Ingestion & Parsing Execution (`app/services/knowledge.py`)
```python
from docling.document_converter import DocumentConverter

class KnowledgeIngestionService:
    def __init__(self):
        self.converter = DocumentConverter()

    def parse_and_chunk(self, file_path: str) -> list:
        # Parse document to structural JSON Representation
        result = self.converter.convert(file_path)
        doc = result.document
        
        # Export structured markdown text
        markdown_text = doc.export_to_markdown()
        raw_chunks = markdown_text.split("\n\n")
        chunks = []
        
        current_heading = "General"
        for raw_chunk in raw_chunks:
            text = raw_chunk.strip()
            if not text:
                continue
                
            # Keep track of header hierarchy to attach metadata
            if text.startswith("#"):
                current_heading = text.lstrip("#").strip()
            
            # Filter noise
            if len(text) < 15:
                continue

            chunks.append({
                "content": text,
                "chunk_index": len(chunks),
                "metadata": {
                    "heading": current_heading,
                    "estimated_length": len(text)
                }
            })
        return chunks
```

---

## 7. RAG Pipeline: In-Depth Engineering Details

```
+---------------+      Docling Parsing      +-------------------+      all-MiniLM-L6-v2      +---------------------+
| Uploaded PDF  | ------------------------> | Structured Chunks | -------------------------> | 384-dim Vectors     |
+---------------+                           +-------------------+                            +---------------------+
                                                                                                        |
                                                                                                        v
                                                                                             +---------------------+
                                                                                             | pgvector Postgres   |
                                                                                             +---------------------+
                                                                                                        ^
                                                                                                        | Cosine Similarity
                                                                                                        v
+---------------+      all-MiniLM-L6-v2      +------------------+      Groq LLM Generation   +---------------------+
| User Question | ------------------------> | Query Vector     | -------------------------> | Answer Generation   |
+---------------+                           +------------------+                             +---------------------+
```

### A. Vector Embedding Model: `all-MiniLM-L6-v2`
- **What is it?**: A SentenceTransformer model fine-tuned on a massive dataset of sentence pairs. It maps inputs to a **384-dimensional dense vector space** capture-matching semantic meaning.
- **Why We Selected It**: 
  - **Dimensionality Efficiency**: OpenAI's `text-embedding-ada-002` maps to 1536 dimensions. Minimizing dimensions to 384 (all-MiniLM-L6-v2) reduces disk space and speeds up vector index scans in PostgreSQL without substantial drops in accuracy.
  - **Local Latency**: Generated locally on CPU via PyTorch in milliseconds, removing latency from external HTTP requests and API costs.

### B. Vector Search & Retrieval
- **pgvector**: We store embeddings inside a PostgreSQL table column with column data type `Vector(384)`.
- **Query Execution**: We perform a Cosine Distance search (`<=>` operator). Cosine distance measures the cosine of the angle between two multi-dimensional vectors, prioritizing semantic similarity over exact word matches:
$$\text{Cosine Distance}(A, B) = 1 - \frac{A \cdot B}{\|A\| \|B\|}$$

### C. LLM Generation
- **Provider**: **Groq API** with model `qwen3.8-27b` (or Llama equivalent).
- **Parameters**: `temperature=0.0` ensures the response is strictly deterministic, reducing conversational style variance. JSON formatting enforces output validity.

---

## 8. RAG Evaluation Framework: Metrics & Scorer

To validate RAG pipelines, we built a custom evaluator using **LLM-as-a-judge** scoring.

### The Four Key Evaluation Metrics

#### 1. Faithfulness (Groundedness)
- **Concept**: Measures if the generated answer is derived *only* from the context. Prevents hallucinations.
- **Math/Scorer Logic**: The LLM splits the answer into individual claims. For each claim, it verifies if it is explicitly stated or logically inferred from the retrieved context.
$$\text{Faithfulness} = \frac{\text{Number of Claims Supported by Context}}{\text{Total Claims in Answer}}$$

#### 2. Answer Relevance
- **Concept**: Measures if the generated answer directly addresses the question, ignoring factual correctness.
- **Math/Scorer Logic**: The LLM evaluates if the answer contains details that satisfy the core query or if it is generic/refusal text.

#### 3. Context Recall
- **Concept**: Measures if the retrieved context contains all necessary facts present in the ground truth.
- **Math/Scorer Logic**: The LLM extracts claims from the reference ground truth and verifies if they can be found within the retrieved context chunks.
$$\text{Context Recall} = \frac{\text{Number of Ground Truth Claims Found in Context}}{\text{Total Claims in Ground Truth}}$$

#### 4. Context Precision
- **Concept**: Measures if the retrieved context is relevant, penalizing noise.
- **Math/Scorer Logic**: Assesses the ratio of relevant chunks within the top-k retrieved results.

---

## 9. Evaluation Runner Implementation

The execution framework compiles evaluations into a markdown summary report:

### Evaluator Code (`app/ai/evaluation/evaluator.py`)
```python
# Location: backend/app/ai/evaluation/evaluator.py
import logging
from typing import Dict, Any
from app.ai.llm.groq_provider import groq_provider

class RAGEvaluator:
    def evaluate_faithfulness(self, question: str, context: str, answer: str) -> Dict[str, Any]:
        prompt = f"""You are an unbiased AI evaluator.
Determine if the generated Answer contains ONLY information that is directly supported by the retrieved Context.
Return a JSON object with keys "score" (float 0.0 to 1.0) and "explanation".

Context:
{context}
Answer:
{answer}
"""
        res = groq_provider.generate(prompt)
        return {"score": float(res.get("score", 0.0)), "explanation": res.get("explanation", "")}
```

### Script Execution Command
To run evaluations, execute the following commands in the workspace terminal:
```bash
cd backend
source venv/bin/activate
python3 run_rag_eval.py
```
This prints the metrics breakdown table:
```
============================================================
                   EVALUATION REPORT
============================================================
| # | Question | Faithfulness | Answer Relevance | Context Precision | Context Recall |
|---|----------|---------------|------------------|-------------------|----------------|
| 1 | Remote work allowance... | 1.00          | 1.00             | 0.90              | 1.00           |
| 2 | Booking training...      | 1.00          | 1.00             | 0.95              | 1.00           |
============================================================
```
This metric framework allows engineers to continuously monitor model configurations, chunking parameters, and vector indexing changes.
