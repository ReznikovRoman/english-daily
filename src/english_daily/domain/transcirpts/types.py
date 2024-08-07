from typing import TypedDict

from english_daily.types import seconds


class TranscriptSequence(TypedDict):
    """Transcript of a sequence in video."""

    text: str
    """Text bound to a timestamp."""

    start: seconds
    """Timestamp, representing the beginning of a text sequence in the video."""

    end: seconds
    """Timestamp, representing the end of a text sequence in the video."""
