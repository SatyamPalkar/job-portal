"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""
    
    # App Settings
    APP_NAME: str = "Resume Optimizer SaaS"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./resume_optimizer.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Hugging Face API
    HUGGINGFACE_API_KEY: str = ""
    HUGGINGFACE_MODEL: str = "mistralai/Mistral-7B-Instruct-v0.2"  # Can also use meta-llama/Llama-2-7b-chat-hf
    
    # Job APIs
    JOOBLE_API_KEY: str = ""  # Get free key from https://jooble.org/api/about
    ADZUNA_APP_ID: str = ""  # Get free key from https://developer.adzuna.com/
    ADZUNA_API_KEY: str = ""
    ADZUNA_COUNTRY: str = "us"  # us, gb, ca, au, etc.
    
    # LinkedIn (optional)
    LINKEDIN_EMAIL: str = ""
    LINKEDIN_PASSWORD: str = ""
    LINKEDIN_CLIENT_ID: str = ""
    LINKEDIN_CLIENT_SECRET: str = ""
    
    # Automation Settings
    AUTO_APPLY_ENABLED: bool = False  # Set to True to enable auto-apply
    DAILY_APPLICATION_LIMIT: int = 50
    APPLICATION_DELAY_MIN: int = 20  # seconds
    APPLICATION_DELAY_MAX: int = 90  # seconds
    ENABLE_JOB_SCHEDULER: bool = False  # Set to True to enable automated job fetching
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # File Upload
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".txt"]
    UPLOAD_DIR: str = "./uploads"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

