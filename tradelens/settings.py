from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    output_dir: str = Field(..., description="Directory to save notes")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
