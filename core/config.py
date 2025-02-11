from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Palli Payment notification system"
    API_V1_STR: str = "/api/v1"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    DOMAIN_NAME: str
    DOMAIN_NAME_2: str
    DOMAIN_LOCAL: str
    ENVIRONMENT: str


    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
