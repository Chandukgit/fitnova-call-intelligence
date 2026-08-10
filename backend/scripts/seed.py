"""Create idempotent local data for the FitNova end-to-end flow.

Run from the backend directory with: python scripts/seed.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select

from app.core.enums import (
    CallStatus,
    CustomerSentiment,
    FeedbackStatus,
    ProcessingStatus,
    Severity,
    UserRole,
)
from app.core.security import get_password_hash
from app.database.session import SessionLocal
from app.models import (
    Advisor,
    Analysis,
    Call,
    Customer,
    Feedback,
    IssueTag,
    Organization,
    Team,
    Transcript,
    User,
)


def get_or_create(db, model, defaults=None, **lookup):
    instance = db.scalar(select(model).filter_by(**lookup))
    if instance:
        return instance
    instance = model(**lookup, **(defaults or {}))
    db.add(instance)
    db.flush()
    return instance


def seed() -> None:
    db = SessionLocal()
    try:
        organization = get_or_create(
            db, Organization, name="FitNova Health", phone="+1-555-0100", email="hello@fitnova.ai"
        )
        sales = get_or_create(db, Team, name="Sales", organization_id=organization.id)
        support = get_or_create(db, Team, name="Support", organization_id=organization.id)

        john = get_or_create(
            db, Advisor,
            employee_id="FN-1001",
            defaults={"team_id": sales.id, "first_name": "John", "last_name": "Carter", "email": "john.carter@fitnova.ai", "phone": "+1-555-0101"},
        )
        sarah = get_or_create(
            db, Advisor,
            employee_id="FN-1002",
            defaults={"team_id": support.id, "first_name": "Sarah", "last_name": "Johnson", "email": "sarah.johnson@fitnova.ai", "phone": "+1-555-0102"},
        )

        get_or_create(
            db, User, email="admin@fitnova.ai",
            defaults={"username": "fitnova_admin", "password_hash": get_password_hash("Admin@123"), "role": UserRole.ADMIN},
        )
        get_or_create(
            db, User, email="manager@fitnova.ai",
            defaults={"username": "support_manager", "password_hash": get_password_hash("Manager@123"), "role": UserRole.MANAGER},
        )
        get_or_create(
            db, User, email="john.carter@fitnova.ai",
            defaults={"username": "john_carter", "password_hash": get_password_hash("Advisor@123"), "role": UserRole.ADVISOR, "advisor_id": john.id},
        )
        get_or_create(
            db, User, email="sarah.johnson@fitnova.ai",
            defaults={"username": "sarah_johnson", "password_hash": get_password_hash("Advisor@123"), "role": UserRole.ADVISOR, "advisor_id": sarah.id},
        )

        alex = get_or_create(db, Customer, phone="+1-555-0201", defaults={"first_name": "Alex", "last_name": "Brown", "email": "alex.brown@example.com", "age": 34, "city": "Austin", "source": "Website"})
        emily = get_or_create(db, Customer, phone="+1-555-0202", defaults={"first_name": "Emily", "last_name": "Davis", "email": "emily.davis@example.com", "age": 29, "city": "Denver", "source": "Referral"})

        call = get_or_create(
            db, Call, original_filename="alex_brown_membership.wav",
            defaults={"advisor_id": john.id, "customer_id": alex.id, "audio_path": "seed/alex_brown_membership.wav", "mime_type": "audio/wav", "file_size": 1024, "duration_seconds": 185, "language": "en", "call_status": CallStatus.COMPLETED, "transcription_status": ProcessingStatus.COMPLETED, "analysis_status": ProcessingStatus.COMPLETED},
        )
        get_or_create(db, Transcript, call_id=call.id, defaults={"transcript": "Advisor: Hello Alex, this is John from FitNova Health.\nCustomer: Hi John, I would like to understand my membership options.\nAdvisor: I can explain the available plans and help you choose the right fit.", "confidence_score": 0.94, "processing_status": ProcessingStatus.COMPLETED})
        analysis = get_or_create(db, Analysis, call_id=call.id, defaults={"overall_score": 88, "needs_discovery_score": 86, "product_knowledge_score": 90, "objection_handling_score": 84, "compliance_score": 92, "next_step_booking_score": 88, "customer_sentiment": CustomerSentiment.POSITIVE, "summary": "John clearly explained membership options and addressed Alex's questions.", "recommendation": "Ask one additional discovery question before recommending a plan.\nConfirm the next step before closing the call.", "processing_status": ProcessingStatus.COMPLETED})
        get_or_create(db, IssueTag, analysis_id=analysis.id, issue_type="Discovery opportunity", defaults={"severity": Severity.LOW, "timestamp": "00:42", "quoted_text": "I can explain the available plans", "reason": "The advisor could ask more about Alex's goals before presenting options."})
        get_or_create(db, Feedback, analysis_id=analysis.id, advisor_comment="I will add more discovery questions.", defaults={"reviewer_comment": "Strong call overall; focus on early discovery.", "status": FeedbackStatus.APPROVED})

        get_or_create(db, Call, original_filename="emily_davis_support.wav", defaults={"advisor_id": sarah.id, "customer_id": emily.id, "audio_path": "seed/emily_davis_support.wav", "mime_type": "audio/wav", "file_size": 1024, "duration_seconds": 143, "language": "en", "call_status": CallStatus.UPLOADED, "transcription_status": ProcessingStatus.PENDING, "analysis_status": ProcessingStatus.PENDING})
        db.commit()
        print("FitNova seed data created or already present.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
