from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated


class Settings(BaseSettings):
    google_cloud_project: str
    location: str
    llm_model_name: str
    max_output_tokens: Annotated[int, Field(gt=0)]
    temperature: Annotated[float, Field(ge=0.0, le=2.0)]
    top_p: Annotated[float, Field(ge=0.0, le=1.0)]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
