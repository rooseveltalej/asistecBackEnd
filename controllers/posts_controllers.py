from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db

# Obtener posts por canal
def get_posts_by_channel(channel_id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.channel_id == channel_id).all()
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found for this channel")

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
    # Verificar si el usuario es admin del canal
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
    return {"msg": "SUCCESS", "post_id": new_post.post_id}
