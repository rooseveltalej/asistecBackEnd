from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db

# Obtener canales a los que el usuario está suscrito
def subscribed_channels(user_id: int, db: Session = Depends(get_db)):
    subscriptions = (
        db.query(models.Subscription)
        .filter(models.Subscription.user_id == user_id)
        .join(models.Channel)
        .all()
    )
    return [
        {
            "channel_id": sub.channel.channel_id,
            "channel_name": sub.channel.channel_name,
            "area_id": sub.channel.area_id,
            "is_admin": sub.is_admin,
            "is_favorite": sub.is_favorite,
        }
        for sub in subscriptions
    ]

# Obtener canales a los que el usuario NO está suscrito
def not_subscribed_channels(user_id: int, db: Session = Depends(get_db)):
    subscribed_ids = (
        db.query(models.Subscription.channel_id)
        .filter(models.Subscription.user_id == user_id)
        .subquery()
    )
    channels = db.query(models.Channel).filter(~models.Channel.channel_id.in_(subscribed_ids)).all()
    return [
        {
            "channel_id": ch.channel_id,
            "channel_name": ch.channel_name,
            "area_id": ch.area_id,
            "is_admin": False,
            "is_favorite": False,
        }
        for ch in channels
    ]

# Obtener todos los posts de un canal específico
def posts_by_channel(channel_id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.channel_id == channel_id).all()
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found for this channel")
    return [
        {
            "post_id": post.post_id,
            "user_id": post.user_id,
            "content": post.content,
            "date": post.date.strftime("%d/%m/%Y %H:%M"),
        }
        for post in posts
    ]

# Crear un nuevo post en un canal
def create_post(user_id: int, post: schemas.PostBase, db: Session = Depends(get_db)):
    new_post = models.Post(
        user_id=user_id,
        channel_id=post.channel_id,
        content=post.content
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"msg": "SUCCESS", "post_id": new_post.post_id}

# Crear un nuevo canal si no existe uno con el mismo nombre
def create_channel(channel: schemas.ChannelBase, db: Session = Depends(get_db)):
    existing = db.query(models.Channel).filter_by(channel_name=channel.channel_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Channel with this name already exists")

    new_channel = models.Channel(**channel.model_dump())
    db.add(new_channel)
    db.commit()
    db.refresh(new_channel)
    return {"msg": "SUCCESS", "channel_id": new_channel.channel_id}
