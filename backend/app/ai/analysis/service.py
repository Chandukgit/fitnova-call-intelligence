from app.ai.prompts.analysis_prompt import (
    analysis_prompt_builder,
)
from app.ai.llm.service import (
    llm_service,
)


class AnalysisService:

    def analyze(
        self,
        transcript: str,
    ) -> dict:

        prompt = analysis_prompt_builder.build(
            transcript
        )

        response = llm_service.analyze(
            prompt
        )

        return response


analysis_service = AnalysisService()