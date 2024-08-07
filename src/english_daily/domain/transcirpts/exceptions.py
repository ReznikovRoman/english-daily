from http import HTTPStatus

from english_daily.common.exceptions import EnglishDailyError


class MissingTranscriptError(EnglishDailyError):
    """Transcript in target language is missing."""

    message = "Transcript in a requested language is missing"
    code = "missing_transcript"
    status_code: int = HTTPStatus.NOT_FOUND
