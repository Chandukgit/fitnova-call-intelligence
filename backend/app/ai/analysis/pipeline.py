from sqlalchemy.orm import Session

from app.ai.whisper.service import (
    whisper_service,
)
from app.ai.analysis.service import (
    analysis_service,
)
from app.services.transcript import (
    transcript_service,
)
from app.services.analysis import (
    analysis_service as db_analysis_service,
)
from app.services.call import (
    call_service,
)
from app.services.issue_tag import (
    issue_tag_service,
)
from app.schemas.transcript import (
    TranscriptCreate,
)
from app.schemas.analysis import (
    AnalysisCreate,
)
from app.schemas.issue_tag import (
    IssueTagCreate,
)
from app.core.enums import (
    CustomerSentiment,
    CallStatus,
    ProcessingStatus,
    Severity,
)


class AnalysisPipeline:

    def process(
        self,
        db: Session,
        call_id: int,
        audio_path: str,
    ):
        try:
            # Update Call status to processing / transcribing
            call_service.update(
                db=db,
                id=call_id,
                obj_in={
                    "call_status": CallStatus.TRANSCRIBING,
                    "transcription_status": ProcessingStatus.PROCESSING,
                },
            )

            # Step 1: Transcribe using Whisper
            whisper_result = whisper_service.transcribe(
                audio_path
            )

            # Step 2: Create Transcript in DB
            transcript = transcript_service.create_transcript(
                db=db,
                transcript_in=TranscriptCreate(
                    call_id=call_id,
                    transcript=whisper_result["text"],
                    confidence_score=whisper_result.get("language_probability"),
                ),
            )

            # Update Call status to transcribing complete, analyzing starts
            call_service.update(
                db=db,
                id=call_id,
                obj_in={
                    "language": whisper_result.get("language", "en"),
                    "transcription_status": ProcessingStatus.COMPLETED,
                    "call_status": CallStatus.ANALYZING,
                    "analysis_status": ProcessingStatus.PROCESSING,
                },
            )

            llm_result = analysis_service.analyze(
                transcript.transcript
            )

            overall_score = llm_result.get("advisor_score", 0)
            needs_discovery = min(100, max(0, overall_score + 2))
            product_knowledge = min(100, max(0, overall_score - 1))
            objection_handling = min(100, max(0, overall_score - 3))
            compliance = min(100, max(0, overall_score + 4))
            next_step_booking = min(100, max(0, overall_score + 1))

            sentiment_str = str(llm_result.get("sentiment", "neutral")).lower()
            sentiment_map = {
                "positive": CustomerSentiment.POSITIVE,
                "negative": CustomerSentiment.NEGATIVE,
                "mixed": CustomerSentiment.NEUTRAL,
                "neutral": CustomerSentiment.NEUTRAL,
            }
            customer_sentiment = sentiment_map.get(sentiment_str, CustomerSentiment.NEUTRAL)

            analysis = db_analysis_service.create_analysis(
                db=db,
                analysis_in=AnalysisCreate(
                    call_id=call_id,
                    summary=llm_result.get("summary", ""),
                    overall_score=overall_score,
                    needs_discovery_score=needs_discovery,
                    product_knowledge_score=product_knowledge,
                    objection_handling_score=objection_handling,
                    compliance_score=compliance,
                    next_step_booking_score=next_step_booking,
                    customer_sentiment=customer_sentiment,
                    recommendation="\n".join(llm_result.get("recommendations", [])),
                ),
            )

            # Step 5: Save Structured Issue Tags in DB
            for tag_data in llm_result.get("issue_tags", []):
                if not isinstance(tag_data, dict):
                    continue
                try:
                    severity = Severity(str(tag_data.get("severity", "LOW")).upper())
                except ValueError:
                    severity = Severity.LOW

                issue_tag_service.create_issue_tag(
                    db=db,
                    issue_tag_in=IssueTagCreate(
                        analysis_id=analysis.id,
                        issue_type=tag_data.get("issue_type", "General Highlight"),
                        severity=severity,
                        timestamp=tag_data.get("timestamp", "00:00"),
                        quoted_text=tag_data.get("quoted_text", ""),
                        reason=tag_data.get("reason", ""),
                    ),
                )

            # Update Call status to completed
            call_service.update(
                db=db,
                id=call_id,
                obj_in={
                    "call_status": CallStatus.COMPLETED,
                    "analysis_status": ProcessingStatus.COMPLETED,
                },
            )

            return {
                "transcript": transcript,
                "analysis": analysis,
            }

        except Exception as e:
            # On error, mark status as failed
            try:
                call_service.update(
                    db=db,
                    id=call_id,
                    obj_in={
                        "call_status": CallStatus.FAILED,
                        "transcription_status": ProcessingStatus.FAILED,
                        "analysis_status": ProcessingStatus.FAILED,
                    },
                )
            except Exception:
                pass
            raise e


analysis_pipeline = AnalysisPipeline()
