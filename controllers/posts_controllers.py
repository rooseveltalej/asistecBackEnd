from fastapi import Depends, HTTPException
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
def create_post(post: schemas.PostBase, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"msg": "SUCCESS", "post_id": new_post.post_id}