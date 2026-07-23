# all environment variables come through here

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool = False
    DATABASE_URL: str 
    UPLOAD_DIR: str 
    CHROMA_PATH: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()