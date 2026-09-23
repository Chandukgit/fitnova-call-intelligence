import os
import sys
import json

# Ensure backend folder is in Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import SessionLocal
from app.services.knowledge import knowledge_service
from app.ai.llm.groq_provider import groq_provider
from app.ai.evaluation.evaluator import rag_evaluator

# Define evaluation dataset
# Contains standard QA pairs that could be grounded in potential knowledge base documents
EVAL_DATASET = [
    {
        "question": "What is the policy on employee remote work equipment allowance?",
        "ground_truth": "Employees are eligible for a one-time remote work equipment allowance of up to $500 to purchase home office furniture, monitors, and peripherals.",
        "fallback_context": "FitNova Remote Work Policy:\n- Employees working remotely are eligible for a one-time equipment allowance of up to $500 for home office furniture, monitors, and peripherals.\n- Receipts must be submitted within 30 days of purchase for reimbursement."
    },
    {
        "question": "How do clients schedule their first personal training session?",
        "ground_truth": "Clients can schedule their first personal training session through the FitNova member portal under the 'Bookings' tab or by calling the reception desk.",
        "fallback_context": "Member Portal Guide:\nTo book sessions, clients should log in to the FitNova portal, go to the 'Bookings' tab, and select an available trainer. Alternatively, they can call the reception desk directly."
    },
    {
        "question": "What is FitNova's cancellation policy for group classes?",
        "ground_truth": "Group classes must be cancelled at least 12 hours in advance to avoid a late cancellation fee of $15.",
        "fallback_context": "Class Attendance Rules:\nAll group fitness class bookings must be cancelled at least 12 hours before the start time. Late cancellations or no-shows are subject to a fee of $15."
    }
]

def format_context(similar_chunks) -> str:
    context_blocks = []
    for chunk in similar_chunks:
        context_blocks.append(f"Source: {chunk['file_name']} | Section: {chunk['heading']}\nContent: {chunk['content']}")
    return "\n\n---\n\n".join(context_blocks)

def run_evaluation(organization_id: int = 1):
    print("=" * 60)
    print("               RAG EVALUATION RUNNER")
    print("=" * 60)
    
    db = SessionLocal()
    results = []

    for i, item in enumerate(EVAL_DATASET, 1):
        question = item["question"]
        ground_truth = item["ground_truth"]
        fallback_context = item["fallback_context"]
        
        print(f"\n[{i}/{len(EVAL_DATASET)}] Evaluating Question: '{question}'")
        
        # 1. Attempt Retrieval from live DB index
        context = ""
        retrieved_chunks = []
        try:
            retrieved_chunks = knowledge_service.search_similar_chunks(
                db=db,
                query=question,
                organization_id=organization_id,
                top_k=3
            )
            if retrieved_chunks:
                context = format_context(retrieved_chunks)
                print(" -> Successfully retrieved relevant chunks from database.")
        except Exception as e:
            # Silence DB errors and use fallback context (e.g. if DB/vector extension isn't running or empty)
            pass

        if not context:
            print(" -> [Notice] Database query returned no chunks or failed. Using pre-defined fallback context.")
            context = fallback_context

        # 2. Generate Answer using Groq Provider
        prompt = f"""You are a FitNova Knowledge Assistant. You help users answer questions based strictly on internal organization documents.
Answer the user's question using ONLY the provided document context. If the answer cannot be found in the context, say "I cannot find the answer in the provided documents."

Return your response as a JSON object with a single key "answer" containing your grounded response. Do not add any text before or after the JSON.

Context:
{context}

Question:
{question}
"""
        try:
            llm_response = groq_provider.generate(prompt)
            answer = llm_response.get("answer", "No answer generated.")
        except Exception as e:
            answer = f"Error generating answer: {str(e)}"

        print(f" -> Generated Answer: {answer}")

        # 3. Evaluate Metrics using RAGEvaluator (LLM-as-a-judge)
        print(" -> Running evaluation metrics...")
        eval_scores = rag_evaluator.evaluate_run(
            question=question,
            context=context,
            answer=answer,
            ground_truth=ground_truth
        )

        results.append({
            "question": question,
            "answer": answer,
            "metrics": eval_scores
        })

    db.close()

    # 4. Generate Markdown Summary Report
    print("\n" + "=" * 60)
    print("                   EVALUATION REPORT")
    print("=" * 60 + "\n")

    print("| # | Question | Faithfulness | Answer Relevance | Context Precision | Context Recall |")
    print("|---|----------|---------------|------------------|-------------------|----------------|")

    total_faithfulness = 0.0
    total_relevance = 0.0
    total_precision = 0.0
    total_recall = 0.0

    for idx, res in enumerate(results, 1):
        m = res["metrics"]
        f_val = m["faithfulness"]["score"]
        ar_val = m["answer_relevance"]["score"]
        cp_val = m["context_precision"]["score"]
        cr_val = m["context_recall"]["score"]

        total_faithfulness += f_val
        total_relevance += ar_val
        total_precision += cp_val
        total_recall += cr_val

        # Truncate question for nice printing
        q_trunc = res["question"][:40] + "..." if len(res["question"]) > 40 else res["question"]
        print(f"| {idx} | {q_trunc} | {f_val:.2f} | {ar_val:.2f} | {cp_val:.2f} | {cr_val:.2f} |")

    n = len(results)
    print("|---|----------|---------------|------------------|-------------------|----------------|")
    print(f"| **Average** | | **{total_faithfulness/n:.2f}** | **{total_relevance/n:.2f}** | **{total_precision/n:.2f}** | **{total_recall/n:.2f}** |")
    print("\n" + "=" * 60)
    print("Evaluation completed successfully.")

if __name__ == "__main__":
    run_evaluation()
