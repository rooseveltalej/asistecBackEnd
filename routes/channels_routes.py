from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db
from controllers.channels_controllers import subscribed_channels, not_subscribed_channels, create_channel, get_all_channels

channel_router = APIRouter(prefix="/api/channels", tags=["Channels"])

@channel_router.get("/subscribed_channels")
def user_subscription_route(user_id: int, db: Session = Depends(get_db)):
    return subscribed_channels(user_id, db)

@channel_router.get("/not_subscribed_channels")
def not_subscribed_channels_route(user_id: int, db: Session = Depends(get_db)):
    return not_subscribed_channels(user_id, db)

@channel_router.get("/all_channels")
def posts_by_channel_route(db: Session = Depends(get_db)):
    return get_all_channels(db)


@channel_router.post("/create_channel", status_code=status.HTTP_201_CREATED)
def create_channel_route(channel: schemas.ChannelBase, db: Session = Depends(get_db)):
    return create_channel(channel, db)