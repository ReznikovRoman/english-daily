from fastapi import APIRouter

from .handlers import misc, transcripts

api_v1_router = APIRouter(prefix="/v1")

api_v1_router.include_router(misc.router)
api_v1_router.include_router(transcripts.router)
