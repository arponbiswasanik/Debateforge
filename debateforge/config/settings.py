from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    groq_api_key: str = ""

    llm_model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 1000
    max_debate_rounds: int = 3

    chroma_persist_directory: str = "./data/chroma"
    yahoo_finance_enabled: bool = True

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False

    log_level: str = "INFO"
    log_file: str = "logs/debateforge.log"

    class Config:
        env_file = ".env"


settings = Settings()