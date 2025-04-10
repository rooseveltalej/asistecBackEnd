from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
import models
import schemas
from database import get_db

# Obtener posts por canal
def get_posts_by_channel(channel_id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.channel_id == channel_id).all()
    
    return [
        {
            "post_id": p.post_id,
            "channel_id": p.channel_id,
            "user_id": p.user_id,
            "content": p.content,
            "date": p.date.strftime("%d/%m/%Y %H:%M")
        }
        for p in posts
    ]


# Crear un nuevo post
def create_post(post: schemas.PostBase, user_id: int, db: Session):
    subscription = db.query(models.Subscription).filter_by(
        user_id=user_id,
        channel_id=post.channel_id,
        is_admin=True
    ).first()

    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para publicar en este canal."
        )

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return JSONResponse(
        content={"msg": "SUCCESS", "post_id": new_post.post_id},
        status_code=status.HTTP_201_CREATED
    )


def get_recent_user_posts(user_id: int, db: Session = Depends(get_db)):
    # Obtener lista de IDs de canales a los que el usuario está suscrito
    subscribed_channel_ids = (
        db.query(models.Subscription.channel_id)
        .filter(models.Subscription.user_id == user_id)
        .subquery()
    )

    # Obtener los 3 posts más recientes de esos canales
    recent_posts = (
        db.query(models.Post.post_id, models.Channel.channel_name)
        .join(models.Channel, models.Post.channel_id == models.Channel.channel_id)
        .filter(models.Post.channel_id.in_(subscribed_channel_ids))
        .order_by(desc(models.Post.date))
        .limit(3)
        .all()
    )

    # Estructurar la respuesta
    return {
        "posts": [
            {
                "post_id": post.post_id,
                "channel_name": post.channel_name
            }
            for post in recent_posts
        ]
    }