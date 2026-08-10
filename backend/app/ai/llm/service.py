from app.ai.llm.groq_provider import (
    groq_provider,
)


class LLMService:

    def analyze(
        self,
        prompt: str,
    ) -> dict:

        return groq_provider.generate(
            prompt
        )


llm_service = LLMService()