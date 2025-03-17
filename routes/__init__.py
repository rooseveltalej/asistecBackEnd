from fastapi import APIRouter
from .users_routes import user_router
from .events_routes import event_router
from .courses_routes import course_router
from .activities_routes import activity_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["Users"])
router.include_router(event_router, prefix="/events", tags=["Events"])
router.include_router(course_router, prefix="/courses", tags=["Courses"])
router.include_router(activity_router, prefix="/activities", tags=["Activities"])