import logging
from typing import Dict, Any, List
from app.ai.llm.groq_provider import groq_provider

logger = logging.getLogger(__name__)

class RAGEvaluator:
    """
    RAG Evaluation Service using LLM-as-a-judge metrics.
    Evaluates key aspects of a RAG pipeline:
    - Faithfulness (Groundedness): Answer is derived ONLY from the retrieved context.
    - Answer Relevance: Answer directly addresses the user's question.
    - Context Recall: Retrieved context contains the information present in the ground truth answer.
    - Context Precision: Retrieved context is relevant to the question (filters out noise).
    """

    def evaluate_faithfulness(self, question: str, context: str, answer: str) -> Dict[str, Any]:
        """
        Measures if the generated answer is faithful to the context and does not contain hallucinations.
        """
        prompt = f"""You are an unbiased AI evaluator assessing RAG (Retrieval-Augmented Generation) system quality.
Analyze the provided user Question, retrieved Context, and generated Answer.
Determine if the generated Answer contains ONLY information that is directly supported by the retrieved Context.
Any facts, statements, or claims in the Answer NOT present in the Context must lower the score.

Return a JSON object with:
1. "score": a float between 0.0 (completely ungrounded/hallucinated) and 1.0 (fully grounded/faithful).
2. "explanation": a concise explanation justifying the score.

Question:
{question}

Context:
{context}

Answer:
{answer}
"""
        try:
            res = groq_provider.generate(prompt)
            return {
                "score": float(res.get("score", 0.0)),
                "explanation": res.get("explanation", "No explanation provided.")
            }
        except Exception as e:
            logger.error(f"Error evaluating faithfulness: {e}")
            return {"score": 0.0, "explanation": f"Evaluation failed: {str(e)}"}

    def evaluate_answer_relevance(self, question: str, answer: str) -> Dict[str, Any]:
        """
        Measures if the generated answer directly and completely addresses the user's question.
        """
        prompt = f"""You are an unbiased AI evaluator assessing RAG system quality.
Analyze the provided user Question and generated Answer.
Determine if the Answer directly addresses the user's Question. The evaluation should focus on completeness, directness, and helpfulness, regardless of factual correctness or context.

Return a JSON object with:
1. "score": a float between 0.0 (completely irrelevant) and 1.0 (perfectly relevant and directly answers the question).
2. "explanation": a concise explanation justifying the score.

Question:
{question}

Answer:
{answer}
"""
        try:
            res = groq_provider.generate(prompt)
            return {
                "score": float(res.get("score", 0.0)),
                "explanation": res.get("explanation", "No explanation provided.")
            }
        except Exception as e:
            logger.error(f"Error evaluating answer relevance: {e}")
            return {"score": 0.0, "explanation": f"Evaluation failed: {str(e)}"}

    def evaluate_context_recall(self, question: str, context: str, ground_truth: str) -> Dict[str, Any]:
        """
        Measures if the retrieved context contains all the necessary information present in the ground truth answer.
        """
        prompt = f"""You are an unbiased AI evaluator assessing RAG system quality.
Analyze the user Question, the retrieved Context, and the reference Ground Truth answer.
Determine if the retrieved Context contains all the necessary facts and details required to formulate the Ground Truth answer.

Return a JSON object with:
1. "score": a float between 0.0 (none of the ground truth facts are in the context) and 1.0 (all ground truth facts are present in the context).
2. "explanation": a concise explanation justifying the score.

Question:
{question}

Context:
{context}

Ground Truth:
{ground_truth}
"""
        try:
            res = groq_provider.generate(prompt)
            return {
                "score": float(res.get("score", 0.0)),
                "explanation": res.get("explanation", "No explanation provided.")
            }
        except Exception as e:
            logger.error(f"Error evaluating context recall: {e}")
            return {"score": 0.0, "explanation": f"Evaluation failed: {str(e)}"}

    def evaluate_context_precision(self, question: str, context: str) -> Dict[str, Any]:
        """
        Measures if the retrieved context contains mostly relevant information for answering the question, penalizing irrelevant noise.
        """
        prompt = f"""You are an unbiased AI evaluator assessing RAG system quality.
Analyze the user Question and the retrieved Context.
Determine if the retrieved Context is highly relevant and precise for answering the Question. If there is a lot of irrelevant noise or unrelated text in the Context, lower the score.

Return a JSON object with:
1. "score": a float between 0.0 (completely irrelevant noise) and 1.0 (fully relevant context with no noise).
2. "explanation": a concise explanation justifying the score.

Question:
{question}

Context:
{context}
"""
        try:
            res = groq_provider.generate(prompt)
            return {
                "score": float(res.get("score", 0.0)),
                "explanation": res.get("explanation", "No explanation provided.")
            }
        except Exception as e:
            logger.error(f"Error evaluating context precision: {e}")
            return {"score": 0.0, "explanation": f"Evaluation failed: {str(e)}"}

    def evaluate_run(self, question: str, context: str, answer: str, ground_truth: str = None) -> Dict[str, Any]:
        """
        Runs evaluation on a single RAG response run.
        """
        results = {
            "faithfulness": self.evaluate_faithfulness(question, context, answer),
            "answer_relevance": self.evaluate_answer_relevance(question, answer),
            "context_precision": self.evaluate_context_precision(question, context),
        }
        if ground_truth:
            results["context_recall"] = self.evaluate_context_recall(question, context, ground_truth)
        return results

rag_evaluator = RAGEvaluator()
