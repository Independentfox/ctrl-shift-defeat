from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosResourceNotFoundError
from config import get_settings
from models.context_object import StartupContextObject

_client = None
_database = None
_sessions_container = None


def _init():
    global _client, _database, _sessions_container
    if _client is not None:
        return
    s = get_settings()
    _client = CosmosClient(s.azure_cosmos_endpoint, credential=s.azure_cosmos_key)
    _database = _client.create_database_if_not_exists(s.azure_cosmos_database)
    _sessions_container = _database.create_container_if_not_exists(
        id="sessions",
        partition_key=PartitionKey(path="/session_id"),
    )


async def save_session(ctx: StartupContextObject) -> None:
    _init()
    doc = ctx.model_dump()
    doc["id"] = ctx.session_id
    _sessions_container.upsert_item(doc)


async def get_session(session_id: str) -> StartupContextObject | None:
    _init()
    try:
        doc = _sessions_container.read_item(item=session_id, partition_key=session_id)
        return StartupContextObject(**doc)
    except CosmosResourceNotFoundError:
        return None


async def delete_session(session_id: str) -> None:
    _init()
    try:
        _sessions_container.delete_item(item=session_id, partition_key=session_id)
    except CosmosResourceNotFoundError:
        pass
