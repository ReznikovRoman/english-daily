import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from english_daily.api.urls import api_router
from english_daily.common.exceptions import EnglishDailyError
from english_daily.core.config import get_settings

from .containers import Container, override_providers

settings = get_settings()


def create_app() -> FastAPI:
    """Фабрика по созданию приложения FastAPI."""
    container = Container()
    json_config = settings.model_dump(mode="json")
    container.config.from_dict(json_config)
    container = override_providers(container)

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        await container.init_resources()  # type:ignore[misc]
        container.check_dependencies()
        logging.info("Start server")
        yield
        await container.shutdown_resources()  # type:ignore[misc]
        logging.info("Cleanup resources")

    app = FastAPI(
        title="English Daily API v1",
        description="АПИ сервиса English Daily.",
        servers=[
            {"url": server_host}
            for server_host in settings.SERVER_HOSTS
        ],
        docs_url=f"{settings.API_V1_STR}/docs",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
        debug=settings.DEBUG,
    )

    @app.exception_handler(EnglishDailyError)
    async def project_exception_handler(_: Request, exc: EnglishDailyError) -> ORJSONResponse:
        return ORJSONResponse(status_code=exc.status_code, content=exc.to_dict())

    app.container = container  # type: ignore[attr-defined]
    app.include_router(api_router)
    return app
