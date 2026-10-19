import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BACKEND_DIR / ".env")


def _env(name: str, default: str = "") -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    return value.strip()


class Settings:
    llm_api_key: str
    llm_base_url: str
    llm_model: str
    llm_timeout_seconds: float
    dataset_path: Path

    def __init__(self) -> None:
        self.llm_api_key = _env("LLM_API_KEY")
        self.llm_base_url = _env("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        self.llm_model = _env("LLM_MODEL", "gpt-4o-mini")
        self.llm_timeout_seconds = float(_env("LLM_TIMEOUT_SECONDS", "60"))
        data_path = Path(_env("DATA_PATH", "data/raw/EV_Adoption_Dataset_Recleaned.xlsx"))
        self.dataset_path = data_path if data_path.is_absolute() else BACKEND_DIR / data_path


settings = Settings()
