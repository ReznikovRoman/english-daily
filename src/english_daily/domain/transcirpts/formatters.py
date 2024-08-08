from __future__ import annotations

import re
from typing import TYPE_CHECKING, ParamSpec

from youtube_transcript_api.formatters import TextFormatter

if TYPE_CHECKING:
    from .types import TranscriptSequence

P = ParamSpec("P")


class VisualTextFormatter(TextFormatter):  # type: ignore[misc]
    """Visual text formatter."""

    def format_transcript(self, transcript: list[TranscriptSequence], *args: P.args, **kwargs: P.kwargs) -> str:
        cleaned_transcript = (
            line["text"].replace("\n", " ")
            for line in transcript
        )
        return self._split_transcript_into_paragraphs(" ".join(cleaned_transcript))

    @staticmethod
    def _split_transcript_into_paragraphs(
        transcript: str, /, *,
        short_paragraph_limit: int = 4,
        long_paragraph_limit: int = 8,
    ) -> str:
        """Split large text into smaller paragraphs for better visualization."""
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
