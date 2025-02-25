from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Settings(BaseSettings):
    # Version
    VERSION: str = "1.0.0"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "postgresql://andrii:cd7131fy@localhost/matchai"
    TEST_DATABASE_URL: str = "sqlite:///./test.db"
    
    # JWT
    SECRET_KEY: str = "cd7131fy-keep-it-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "MatchAI"

    FACEBOOK_CLIENT_ID: str
    FACEBOOK_CLIENT_SECRET: str
    TWITTER_CLIENT_ID: str
    TWITTER_CLIENT_SECRET: str

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"
    )

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://andrii@localhost:5432/fastapi_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

settings = Settings()
