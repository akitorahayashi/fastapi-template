from fastapi import APIRouter

from src.api.v1.routers import item_router

api_router = APIRouter()
api_router.include_router(item_router.router)
