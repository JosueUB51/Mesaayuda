from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    ENV: str

    OPENROUTER_API_KEY: str
    OPENROUTER_MODEL: str
    OPENROUTER_BASE_URL: str

    DB_URL: str
    TICKET_PREFIX: str

    class Config:
        env_file = ".env"

settings = Settings()
