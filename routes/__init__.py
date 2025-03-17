from fastapi import APIRouter
from .users_routes import user_router
from .events_routes import event_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["Users"])
router.include_router(event_router, prefix="/events", tags=["Events"])