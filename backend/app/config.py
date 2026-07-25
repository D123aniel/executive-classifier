from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Executive Evasiveness Classifier"
    model_path: Path = Path("/models/best_model")
    allowed_origins: str = "http://localhost:4200"
    top_score_review_threshold: float = 0.60
    margin_review_threshold: float = 0.15
    max_text_characters: int = 12_000

    @property
    def origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.allowed_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
