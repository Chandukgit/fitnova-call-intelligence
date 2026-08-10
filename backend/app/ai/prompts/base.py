from abc import ABC, abstractmethod


class PromptBuilderBase(ABC):

    @abstractmethod
    def build(
        self,
        transcript: str,
    ) -> str:
        pass