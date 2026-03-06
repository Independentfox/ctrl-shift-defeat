from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from config import get_settings


def _get_blob_service() -> BlobServiceClient:
    s = get_settings()
    return BlobServiceClient.from_connection_string(s.azure_storage_connection_string)


async def upload_file(data: bytes, blob_name: str, content_type: str = "application/octet-stream") -> str:
    s = get_settings()
    service = _get_blob_service()
    container = service.get_container_client(s.azure_storage_container_outputs)
    try:
        container.create_container()
    except Exception:
        pass

    blob = container.get_blob_client(blob_name)
    blob.upload_blob(data, overwrite=True, content_settings={"content_type": content_type})
    return blob.url


async def get_download_url(blob_name: str) -> str:
    s = get_settings()
    service = _get_blob_service()
    account_name = service.account_name

    sas = generate_blob_sas(
        account_name=account_name,
        container_name=s.azure_storage_container_outputs,
        blob_name=blob_name,
        account_key=service.credential.account_key if hasattr(service.credential, "account_key") else s.azure_storage_connection_string.split("AccountKey=")[1].split(";")[0],
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1),
    )
    return f"https://{account_name}.blob.core.windows.net/{s.azure_storage_container_outputs}/{blob_name}?{sas}"
