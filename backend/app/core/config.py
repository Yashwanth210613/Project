from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Clinical AI CDS API"
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60

    database_url: str = "sqlite:///./clinical.db"

    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    s3_bucket_name: str = ""

    hf_model_name: str = "distilgpt2"

    class Config:
        env_file = ".env"


settings = Settings()
