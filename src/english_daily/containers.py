from dependency_injector import containers, providers

from english_daily.core.config import get_settings
from english_daily.core.logging import configure_logger
from english_daily.domain import transcirpts

settings = get_settings()


class Container(containers.DeclarativeContainer):
    """Контейнер с зависимостями."""

    wiring_config = containers.WiringConfiguration(
        packages=[
            "english_daily.api.v1.handlers",
        ],
    )

    config = providers.Configuration()
    json_config = settings.model_dump(mode="json")
    config.from_dict(json_config)

    logging = providers.Resource(configure_logger)

    # Domain -> Transcripts
    transcript_visual_formatter = providers.Factory(transcirpts.VisualTextFormatter)

    transcript_service = providers.Singleton(
        transcirpts.TranscriptService,
        formatter=transcript_visual_formatter,
    )


def override_providers(container: Container) -> Container:
    """Перезаписывание провайдеров с помощью стабов."""
    if not container.config.USE_STUBS():
        return container
    return container


async def dummy_resource() -> None:
    """Функция-ресурс для перезаписи в DI контейнере."""
