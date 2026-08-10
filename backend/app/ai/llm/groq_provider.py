import json

from groq import Groq

from app.ai.llm.base import LLMBase
from app.core.config import settings


class GroqProvider(LLMBase):

    def __init__(self):

        self.client = Groq(
            api_key=settings.GROQ_API_KEY,
        )

        self.model = "llama-3.3-70b-versatile"

    def generate(
        self,
        prompt: str,
    ) -> dict:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
            response_format={
                "type": "json_object",
            },
        )

        content = response.choices[0].message.content

        return json.loads(content)


groq_provider = GroqProvider()