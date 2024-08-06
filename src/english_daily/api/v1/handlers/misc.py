from fastapi import APIRouter

router = APIRouter(
    tags=["Misc"],
)


@router.get("/healthcheck", summary="'Здоровье' сервиса")
async def healthcheck() -> dict:
    """Проверка состояния сервиса."""
    return {"status": "ok"}
