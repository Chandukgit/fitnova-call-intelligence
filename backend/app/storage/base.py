from abc import ABC, abstractmethod
from pathlib import Path


class StorageBase(ABC):

    @abstractmethod
    def save_file(
        self,
        file_bytes: bytes,
        file_path: str,
    ) -> Path:
        pass

    @abstractmethod
    def delete_file(
        self,
        file_path: str,
    ) -> None:
        pass

    @abstractmethod
    def file_exists(
        self,
        file_path: str,
    ) -> bool:
        pass