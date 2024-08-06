from __future__ import annotations

from fastapi import APIRouter

from english_daily.domain.transcripts import fetch_english_transcript

router = APIRouter(tags=["Transcripts"])


@router.get(
    path="/transcripts/{video_id}",
    summary="Получение транскрипта видео",
)
async def get_transcript(video_id: str) -> dict:
    transcript = await fetch_english_transcript(video_id)
    print("TEST: ", transcript)  # noqa: T201: TODO: remove
    return {"transcript": transcript}
