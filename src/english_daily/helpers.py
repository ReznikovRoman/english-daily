import re
from collections.abc import Iterator
from typing import Any
from zoneinfo import ZoneInfo

SLUG_REGEX = re.compile(r"^[-\w]+$")

TZ_MOSCOW = ZoneInfo("Europe/Moscow")

sentinel: Any = object()


def resolve_callables(mapping: dict) -> Iterator[tuple[Any, Any]]:
    """Генерация пар ключ-значение из `mapping`, где значения могут быть callable объектами."""
    for key, value in mapping.items():
        yield key, value() if callable(value) else value
