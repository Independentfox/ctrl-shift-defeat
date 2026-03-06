from fastapi import APIRouter, HTTPException
from models.api_models import DownloadResponse
from storage import cosmos_client, blob_client

router = APIRouter(prefix="/api/output", tags=["download"])


@router.get("/download", response_model=DownloadResponse)
async def download_output(session_id: str, file_type: str):
    ctx = await cosmos_client.get_session(session_id)
    if not ctx:
        raise HTTPException(status_code=404, detail="Session not found")

    if file_type == "pitch_deck":
        blob_name = f"{session_id}/pitch_deck.pptx"
    elif file_type == "financial_model":
        blob_name = f"{session_id}/financial_model.xlsx"
    elif file_type == "roadmap":
        blob_name = f"{session_id}/roadmap.pdf"
    else:
        raise HTTPException(status_code=400, detail=f"Invalid file_type: {file_type}")

    try:
        url = await blob_client.get_download_url(blob_name)
        return DownloadResponse(download_url=url, file_type=file_type)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"File not found: {e}")
