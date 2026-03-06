"""Embed documents and upload to Azure AI Search indexes."""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex
from azure.core.credentials import AzureKeyCredential
from google import genai
from dotenv import load_dotenv
import os

load_dotenv(Path(__file__).parent.parent.parent / ".env")

SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("AZURE_SEARCH_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "text-embedding-004")

DATA_DIR = Path(__file__).parent.parent.parent / "data" / "processed"
SCHEMA_DIR = Path(__file__).parent.parent.parent / "infra" / "search_index_schemas"

gemini_client = genai.Client(api_key=GEMINI_KEY)

index_client = SearchIndexClient(
    endpoint=SEARCH_ENDPOINT,
    credential=AzureKeyCredential(SEARCH_KEY),
)


def get_embedding(text: str) -> list[float]:
    result = gemini_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text[:2000],
    )
    return result.embeddings[0].values


def create_index(schema_path: Path):
    schema = json.loads(schema_path.read_text())
    print(f"Creating index: {schema['name']}")
    try:
        index_client.create_or_update_index(SearchIndex.from_dict(schema))
        print(f"  Index '{schema['name']}' ready.")
    except Exception as e:
        print(f"  Error: {e}")


def upload_documents(index_name: str, docs: list[dict]):
    search_client = SearchClient(
        endpoint=SEARCH_ENDPOINT,
        index_name=index_name,
        credential=AzureKeyCredential(SEARCH_KEY),
    )

    # Embed in batches
    for i, doc in enumerate(docs):
        content = doc.get("content", "")
        if not content:
            content = " ".join(str(v) for k, v in doc.items() if k not in ("id", "embedding") and v)
            doc["content"] = content

        print(f"  Embedding doc {i+1}/{len(docs)}: {doc.get('id', 'unknown')[:40]}")
        doc["embedding"] = get_embedding(content)
        time.sleep(0.1)  # Rate limiting for Gemini free tier

    # Upload in batches of 100
    for batch_start in range(0, len(docs), 100):
        batch = docs[batch_start:batch_start + 100]
        result = search_client.upload_documents(batch)
        succeeded = sum(1 for r in result if r.succeeded)
        print(f"  Uploaded batch: {succeeded}/{len(batch)} succeeded")


def main():
    # Create indexes
    for schema_file in SCHEMA_DIR.glob("*.json"):
        create_index(schema_file)

    # Upload data
    for data_file in DATA_DIR.glob("*.json"):
        index_name = data_file.stem.replace("_", "-")
        print(f"\nProcessing {data_file.name} -> index '{index_name}'")
        docs = json.loads(data_file.read_text())
        if not isinstance(docs, list):
            docs = [docs]
        upload_documents(index_name, docs)

    print("\nAll indexes populated!")


if __name__ == "__main__":
    main()
