from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Google Gemini (FREE)
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    gemini_embedding_model: str = "text-embedding-004"

    # Azure AI Search
    azure_search_endpoint: str = ""
    azure_search_api_key: str = ""

    # Azure Cosmos DB
    azure_cosmos_endpoint: str = ""
    azure_cosmos_key: str = ""
    azure_cosmos_database: str = "cofounder_db"

    # Azure Blob Storage
    azure_storage_connection_string: str = ""
    azure_storage_container_outputs: str = "outputs"

    # App
    frontend_url: str = "http://localhost:5173"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
