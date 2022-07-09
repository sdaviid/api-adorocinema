from fastapi import APIRouter
from app.api.routes import route_title


api_router = APIRouter()
api_router.include_router(route_title.router, prefix="/title", tags=["title"])

