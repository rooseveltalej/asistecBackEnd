from fastapi import APIRouter
from .users_routes import user_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["Users"])
