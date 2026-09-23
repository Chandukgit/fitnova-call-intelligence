from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    question: str
    chat_history: Optional[List[dict]] = None

class SourceCitation(BaseModel):
    file_name: str
    heading: str
    chunk_index: int

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceCitation]
