from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.organization import router as organization_router
from app.api.routers.team import router as team_router
from app.api.routers.advisor import router as advisor_router
from app.api.routers.customer import router as customer_router
from app.api.routers.call import router as call_router
from app.api.routers.transcript import router as transcript_router
from app.api.routers.analysis import router as analysis_router
from app.api.routers.issue_tag import router as issue_tag_router
from app.api.routers.feedback import router as feedback_router
from app.api.routers.user import router as user_router
from app.core.handlers import register_exception_handlers
from app.api.routers.auth import router as auth_router
from app.api.routers.upload import router as upload_router


app = FastAPI(
    title="FitNova Call Intelligence API",
    description="Backend APIs for FitNova AI Call Intelligence Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register global exception handlers
register_exception_handlers(app)

# Register all API routers
app.include_router(organization_router)
app.include_router(team_router)
app.include_router(advisor_router)
app.include_router(customer_router)
app.include_router(call_router)
app.include_router(transcript_router)
app.include_router(analysis_router)
app.include_router(issue_tag_router)
app.include_router(feedback_router)

app.include_router(auth_router)

app.include_router(user_router)

app.include_router(upload_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to FitNova Call Intelligence API 🚀"
    }
