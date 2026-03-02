from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
import schemas
from database import get_db
from controllers.posts_controllers import (
    get_posts_by_channel,
    create_post,
    update_post,
    delete_post,
    get_recent_user_posts,
)

post_router = APIRouter(prefix="/api/posts", tags=["Posts"])

@post_router.get("/by_channel", response_model=list[schemas.PostResponse])
def get_posts_by_channel_route(channel_id: int, db: Session = Depends(get_db)):
    return get_posts_by_channel(channel_id, db)

@post_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=dict)
def create_post_route(post: schemas.PostBase, db: Session = Depends(get_db)):
    return create_post(post, post.user_id, db)

@post_router.put("/update/{post_id}", response_model=dict)
def update_post_route(post_id: int, user_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    return update_post(post_id, user_id, post, db)

@post_router.delete("/delete/{post_id}", response_model=dict)
def delete_post_route(post_id: int, user_id: int, db: Session = Depends(get_db)):
    return delete_post(post_id, user_id, db)

@post_router.get("/user_recent_posts", response_model=List[schemas.PostResponse])
def get_recent_user_posts_route(user_id: int, db: Session = Depends(get_db)):
    return get_recent_user_posts(user_id, db)
