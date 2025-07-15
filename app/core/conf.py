from pathlib import Path
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    db_user: str
    db_pass: str
    db_name: str
    db_port: str
    db_host: str

    token_secret: str

    media_files_path: Path = BASE_DIR / "media"

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"

settings = Settings()
