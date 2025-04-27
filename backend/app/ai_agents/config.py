from pydantic_settings import BaseSettings

class AIConfig(BaseSettings):
    OPENAI_API_KEY: str
    GPT_MODEL: str = "gpt-3.5-turbo"
    MAX_TOKENS: int = 500
    TEMPERATURE: float = 0.3
    
    class Config:
        env_file = ".env"
