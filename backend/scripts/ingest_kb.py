import os
import sys
from pathlib import Path

# Add backend directory to path so we can import app modules
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database.session import SessionLocal
from app.services.knowledge import knowledge_service
from app.models.organization import Organization

def run_bulk_ingestion():
    db = SessionLocal()
    try:
        # Find the default organization (seeded by seed.py)
        org = db.query(Organization).filter(Organization.name == "FitNova Health").first()
        if not org:
            print("ERROR: Organization 'FitNova Health' not found. Please run: python scripts/seed.py first!")
            return
            
        kb_path = "/Users/chandukiliveti/Downloads/fitnova_raw_knowledge_base_500"
        if not os.path.exists(kb_path):
            print(f"ERROR: Raw data folder not found at {kb_path}")
            return

        print(f"Starting bulk ingestion of documents from {kb_path} (Org ID: {org.id})")
        
        supported_extensions = {".pdf", ".docx", ".xlsx", ".csv", ".txt", ".md", ".png"}
        
        success_count = 0
        skipped_count = 0
        error_count = 0
        
        # Traverse recursively
        for root, dirs, files in os.walk(kb_path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in supported_extensions:
                    file_path = os.path.join(root, file)
                    print(f"Processing: {file_path}")
                    try:
                        doc = knowledge_service.ingest_document(
                            db=db, 
                            file_path=file_path, 
                            organization_id=org.id
                        )
                        success_count += 1
                    except Exception as e:
                        print(f"Error ingesting {file_path}: {e}")
                        error_count += 1
                        
        print("\n=== Ingestion Summary ===")
        print(f"Successfully processed: {success_count}")
        print(f"Failed to process: {error_count}")
        print("=========================")
        
    finally:
        db.close()

if __name__ == "__main__":
    run_bulk_ingestion()
