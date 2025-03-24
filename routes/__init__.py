from fastapi import APIRouter
from .users_routes import user_router
from .events_routes import event_router
from .courses_routes import course_router
from .activities_routes import activity_router
from .channels_routes import channel_router
from .areas_routes import area_router
from .subscriptions_routes import subscription_router

router = APIRouter()

router.include_router(user_router, tags=["Users"])
router.include_router(event_router, tags=["Events"])
router.include_router(course_router, tags=["Courses"])
router.include_router(activity_router, tags=["Activities"])
router.include_router(channel_router, tags=["Channels"])
router.include_router(area_router, tags=["Areas"])
router.include_router(subscription_router, tags=["Subscriptions"])