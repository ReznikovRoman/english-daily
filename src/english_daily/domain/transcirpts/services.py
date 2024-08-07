from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, cast

from youtube_transcript_api import NoTranscriptFound, YouTubeTranscriptApi

from .constants import TranscriptLanguageList
from .exceptions import MissingTranscriptError

if TYPE_CHECKING:
    from youtube_transcript_api._transcripts import Transcript
    from youtube_transcript_api.formatters import Formatter


class TranscriptService:
    def __init__(self, formatter: Formatter) -> None:
        self._formatter = formatter

    async def load_transcript(
        self,
        video_id: str, /, *,
        target_language: TranscriptLanguageList = TranscriptLanguageList.english,
    ) -> str:
        """Load video transcript."""
        # TODO: store generated transcript in Redis with a given TTL
        translated_transcript = await self.fetch_transcript(video_id, target_language=target_language)
        transcript = await asyncio.to_thread(translated_transcript.fetch)
        return cast("str", self._formatter.format_transcript(transcript))

    async def fetch_transcript(
        self,
        video_id: str, /, *,
        target_language: TranscriptLanguageList = TranscriptLanguageList.english,
    ) -> Transcript:
        """Fetch transcript from YouTube."""
        # TODO: write a custom async version of `YouTubeTranscriptApi` for fetching transcripts using aiohttp
        transcripts = await asyncio.to_thread(YouTubeTranscriptApi.list_transcripts, video_id)
        try:
            return cast("Transcript", transcripts.find_manually_created_transcript((target_language,)))
        except NoTranscriptFound:
            # TODO: mark video/transcript as auto-generated for future downloads
            logging.info(
                "No manual transcript found for video <%s>, searching for an auto-generated one.", video_id)
        try:
            return cast("Transcript", transcripts.find_generated_transcript((target_language,)))
        except NoTranscriptFound as exc:
            # TODO: mark video as disabled since there is no transcript
            logging.info(
                "No transcript in target language <%s> found for video <%s>.", target_language, video_id)
            raise MissingTranscriptError from exc
