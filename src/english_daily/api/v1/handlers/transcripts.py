from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject

from fastapi import APIRouter, Depends

from english_daily.containers import Container

if TYPE_CHECKING:
    from english_daily.domain.transcirpts import TranscriptService

router = APIRouter(tags=["Transcripts"])


@router.get(
    path="/transcripts/{video_id}",
    summary="Получение транскрипта видео",
)
@inject
async def get_transcript(
    video_id: str, *,
    transcript_service: TranscriptService = Depends(Provide[Container.transcript_service]),
) -> dict:
    # Example transcripts:
    # - Works fine, formatter works: SoP_lJ0FWoc
    # - Formatting does not work: ZAhRuuNG_BY TODO: fix formatter
    transcript = await transcript_service.load_transcript(video_id)
    print("TEST: ", transcript)  # noqa: T201: TODO: remove
    return {"transcript": transcript}
