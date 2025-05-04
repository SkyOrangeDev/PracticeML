from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Bot settings
    BOT_TOKEN: str
    ADMIN_IDS: List[int]
    MAX_MESSAGE_LENGTH: int = 4096
    
    # OpenAI settings
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 150
    
    # Database settings
    DATABASE_URL: str = "sqlite:///bot.db"
    
    # Cache settings
    CACHE_TTL: int = 3600  # 1 hour
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    @classmethod
    def parse_admin_ids(cls, admin_ids_str: str) -> List[int]:
        return [int(admin_id.strip()) for admin_id in admin_ids_str.split(",")]

settings = Settings(
    ADMIN_IDS=Settings.parse_admin_ids(os.getenv("ADMIN_IDS", ""))
) 