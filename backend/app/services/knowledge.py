import os
import hashlib
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from docling.document_converter import DocumentConverter
from sentence_transformers import SentenceTransformer
from app.models.knowledge import Document, DocumentChunk
from sqlalchemy import select

class KnowledgeIngestionService:
    def __init__(self):
        # Using a widely-used open-source Meta model (384 dimensions)
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.converter = DocumentConverter()

    def get_file_hash(self, file_path: str) -> str:
        """Generate SHA-256 hash of file contents for change/duplicate detection."""
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def parse_and_chunk(self, file_path: str) -> List[Dict[str, Any]]:
        """Parses document using Docling and creates section-aware chunks."""
        # Convert document to structured representation
        result = self.converter.convert(file_path)
        doc = result.document
        
        # Export structured layout to Markdown
        markdown_text = doc.export_to_markdown()
        
        # Split document by markdown headings or paragraphs
        raw_chunks = markdown_text.split("\n\n")
        chunks = []
        
        current_heading = "General"
        for i, raw_chunk in enumerate(raw_chunks):
            text = raw_chunk.strip()
            if not text:
                continue
                
            # If this is a markdown header, update current context
            if text.startswith("#"):
                current_heading = text.lstrip("#").strip()
            
            # Simple chunk validation: skip very short noise
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

    def ingest_document(self, db: Session, file_path: str, organization_id: int) -> Document:
        """Main entry point: detects duplicates, runs Docling, generates embeddings, stores to DB."""
        file_name = os.path.basename(file_path)
        file_type = os.path.splitext(file_name)[1].lower().replace(".", "")
        file_hash = self.get_file_hash(file_path)

        # 1. Deduplication / Version Update check
        existing_doc = db.query(Document).filter(Document.file_hash == file_hash).first()
        if existing_doc:
            # Document hasn't changed, skip reprocessing
            return existing_doc

        # Check if a document with the same name exists (we will replace it)
        old_doc = db.query(Document).filter(
            Document.file_name == file_name, 
            Document.organization_id == organization_id
        ).first()
        if old_doc:
            db.delete(old_doc)
            db.commit()

        # 2. Parse heterogeneous document using Docling
        parsed_chunks = self.parse_and_chunk(file_path)

        # 3. Create Document entry
        new_doc = Document(
            organization_id=organization_id,
            file_name=file_name,
            file_type=file_type,
            file_hash=file_hash,
            title=file_name
        )
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)

        # 4. Generate embeddings and save chunks
        for pc in parsed_chunks:
            # Vector embedding generation (runs locally on CPU)
            emb = self.embedding_model.encode(pc["content"]).tolist()
            
            chunk = DocumentChunk(
                document_id=new_doc.id,
                content=pc["content"],
                embedding=emb,
                metadata_json=pc["metadata"],
                chunk_index=pc["chunk_index"]
            )
            db.add(chunk)
            
        db.commit()
        return new_doc

    def search_similar_chunks(self, db: Session, query: str, organization_id: int, top_k: int = 5) -> List[Dict[str, Any]]:
        """Encodes user query and retrieves top_k most similar document chunks, filtered by org."""
        # 1. Encode query to vector
        query_vector = self.embedding_model.encode(query).tolist()

        # 2. Query document chunks and join with documents to filter by organization_id
        # <=> is the cosine distance operator in pgvector. Distance ASC means similarity DESC.
        stmt = (
            select(DocumentChunk, Document)
            .join(Document, DocumentChunk.document_id == Document.id)
            .where(Document.organization_id == organization_id)
            .order_by(DocumentChunk.embedding.cosine_distance(query_vector))
            .limit(top_k)
        )
        
        results = db.execute(stmt).all()
        
        retrieved_chunks = []
        for chunk, doc in results:
            retrieved_chunks.append({
                "chunk_id": chunk.id,
                "content": chunk.content,
                "file_name": doc.file_name,
                "heading": chunk.metadata_json.get("heading", "General"),
                "chunk_index": chunk.chunk_index
            })
            
        return retrieved_chunks

    
knowledge_service = KnowledgeIngestionService()
