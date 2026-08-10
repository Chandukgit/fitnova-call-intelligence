from pathlib import Path

from app.storage.base import StorageBase


class LocalStorage(StorageBase):

    def __init__(
        self,
        upload_dir: str = "uploads",
    ):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save_file(
        self,
        file_bytes: bytes,
        file_path: str,
    ) -> Path:

        destination = self.upload_dir / file_path

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(destination, "wb") as file:
            file.write(file_bytes)

        return destination

    def delete_file(
        self,
        file_path: str,
    ) -> None:

        destination = self.upload_dir / file_path

        if destination.exists():
            destination.unlink()

    def file_exists(
        self,
        file_path: str,
    ) -> bool:

        return (
            self.upload_dir / file_path
        ).exists()


storage = LocalStorage()