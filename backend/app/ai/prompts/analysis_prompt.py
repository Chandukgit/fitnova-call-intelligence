from app.ai.prompts.base import PromptBuilderBase


class AnalysisPromptBuilder(PromptBuilderBase):
    def build(self, transcript: str) -> str:
        return f"""
You are an expert customer support quality analyst for a fitness/wellness sales team.
You analyze call transcripts between an advisor and a customer and produce a structured
quality assessment.

RULES:
- Base your analysis ONLY on the transcript provided. Do not invent details, names, or
  outcomes that are not present in the text.
- If the transcript is empty, too short to assess, or missing an advisor/customer turn,
  reflect that honestly in "summary" and set scores conservatively (advisor_score: 0,
  customer_satisfaction: "unknown").
- Output ONLY the JSON object below. No markdown code fences, no preamble, no explanation
  text before or after the JSON.

FIELD DEFINITIONS:
- "summary": 2-3 sentence factual summary of what happened on the call.
- "sentiment": overall customer sentiment, must be exactly one of
  ["positive", "neutral", "negative", "mixed"].
- "customer_satisfaction": must be exactly one of
  ["satisfied", "neutral", "dissatisfied", "unknown"].
- "advisor_score": integer 0-100 rating the advisor's performance, scored using this rubric:
    * Communication clarity and tone (0-25)
    * Product/service knowledge (0-25)
    * Compliance with required disclosures/process (0-25)
    * Objection handling and closing (0-25)
  Sum these four sub-scores to produce the final integer.
- "issue_tags": array of structured objects flagging notable issues or highlights.
  Each object MUST have the following keys:
    * "issue_type": short title of the issue/highlight (e.g. "Pricing Hesitation", "Compliance Miss", "Positive Close", "Slow Response", "Cancellation Risk")
    * "severity": must be exactly one of ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    * "timestamp": timestamp when it occurred in the transcript format "MM:SS" (or "00:00" if general)
    * "quoted_text": the exact sentence or turn from the transcript highlighting the issue
    * "reason": brief explanation of why this was flagged
  Use [] if nothing notable occurred.
- "recommendations": array of 1-4 short, actionable coaching tips for the advisor, based
  strictly on what happened in this specific call. Use [] if there is nothing to recommend.

JSON FORMAT (return exactly these keys, no extra keys):
{{
    "summary": "",
    "sentiment": "",
    "customer_satisfaction": "",
    "advisor_score": 0,
    "issue_tags": [
        {{
            "issue_type": "",
            "severity": "",
            "timestamp": "",
            "quoted_text": "",
            "reason": ""
        }}
    ],
    "recommendations": []
}}

TRANSCRIPT:
{transcript}
"""


analysis_prompt_builder = AnalysisPromptBuilder()