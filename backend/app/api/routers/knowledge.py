from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.knowledge import ChatRequest, ChatResponse, SourceCitation
from app.services.knowledge import knowledge_service
from app.ai.llm.groq_provider import groq_provider

router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge Base"],
)

def get_user_org_id(user: User) -> int:
    """Helper to retrieve organization_id from the user's relations."""
    if not user.advisor or not user.advisor.team:
        # Default fallback to first organization if advisor information is missing (e.g. admin accounts)
        return 1
    return user.advisor.team.organization_id

@router.post("/chat", response_model=ChatResponse)
def chat_with_knowledge(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    org_id = get_user_org_id(current_user)
    
    # 1. Retrieve the top 5 most similar document chunks
    similar_chunks = knowledge_service.search_similar_chunks(
        db=db,
        query=request.question,
        organization_id=org_id,
        top_k=5
    )

    if not similar_chunks:
        return ChatResponse(
            answer="I'm sorry, I couldn't find any documents related to your query in the FitNova Knowledge Base.",
            sources=[]
        )

    # 2. Build context text
    context_blocks = []
    for chunk in similar_chunks:
        context_blocks.append(f"Source: {chunk['file_name']} | Section: {chunk['heading']}\nContent: {chunk['content']}")
    
    context_str = "\n\n---\n\n".join(context_blocks)

    # 3. Create prompt for Groq LLM (llama-3.3-70b-versatile, outputting JSON as configured in groq_provider)
    prompt = f"""You are a FitNova Knowledge Assistant. You help users answer questions based strictly on internal organization documents.
Answer the user's question using ONLY the provided document context. If the answer cannot be found in the context, say "I cannot find the answer in the provided documents."

Return your response as a JSON object with a single key "answer" containing your grounded response. Do not add any text before or after the JSON.

Context:
{context_str}

Question:
{request.question}
"""

    try:
        # Re-use the existing groq_provider that parses responses to dict automatically
        llm_response = groq_provider.generate(prompt)
        answer = llm_response.get("answer", "No answer could be generated.")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating response from LLM: {str(e)}"
        )

    # 4. Compile citations
    sources = []
    seen_sources = set()
    for chunk in similar_chunks:
        source_key = (chunk["file_name"], chunk["heading"])
        if source_key not in seen_sources:
            seen_sources.add(source_key)
            sources.append(SourceCitation(
                file_name=chunk["file_name"],
                heading=chunk["heading"],
                chunk_index=chunk["chunk_index"]
            ))

    return ChatResponse(answer=answer, sources=sources)
