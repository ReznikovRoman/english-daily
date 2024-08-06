from __future__ import annotations

import asyncio
import logging
import re
from typing import TYPE_CHECKING, ParamSpec, cast

from youtube_transcript_api import NoTranscriptFound, YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

if TYPE_CHECKING:
    from youtube_transcript_api import Transcript

P = ParamSpec("P")


class VisualTextFormatter(TextFormatter):  # type: ignore[misc]
    def format_transcript(self, transcript: list[dict[str, str]], *args: P.args, **kwargs: P.kwargs) -> str:
        cleaned_transcript = (
            line["text"].replace("\n", " ")
            for line in transcript
        )
        return self._split_transcript_into_paragraphs(" ".join(cleaned_transcript))

    def _split_transcript_into_paragraphs(
        self,
        transcript: str, /, *,
        short_paragraph_limit: int = 4,
        long_paragraph_limit: int = 8,
    ) -> str:
        sentences = re.split(r"(?<=[.!?]) +", transcript)
        paragraphs = []
        current_paragraph = []
        for sentence in sentences:
            current_paragraph.append(sentence)
            if len(current_paragraph) == short_paragraph_limit:
                paragraphs.append(" ".join(current_paragraph))
                current_paragraph = []
            elif len(current_paragraph) >= long_paragraph_limit:
                paragraphs.append("\n".join(current_paragraph))
                current_paragraph = []

        if current_paragraph:
            paragraphs.append(" ".join(current_paragraph))

        return "\n\n".join(paragraphs)


async def fetch_english_transcript(video_id: str, /) -> str:
    """Загрузка транскрипта к видео."""
    # TODO: store generated transcript in Redis for a given TTL

    formatter = VisualTextFormatter()

    transcripts = await asyncio.to_thread(YouTubeTranscriptApi.list_transcripts, video_id)

    try:
        translated_transcript = cast("Transcript", transcripts.find_manually_created_transcript(("ru",)))
    except NoTranscriptFound:
        # TODO: mark video as auto generated for future downloads
        logging.info("No manual transcript found for video <%s>, using auto-generated one.", video_id)
        translated_transcript = cast("Transcript", transcripts.find_generated_transcript(("en",)))

    transcript = await asyncio.to_thread(translated_transcript.fetch)

    return formatter.format_transcript(transcript)
