from abc import ABC, abstractmethod


class LLMBase(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> dict:
        """
        Generate a response from the LLM.
        """
        pass
