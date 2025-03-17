from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db


def user_subscription(user_id: int, db: Session = Depends(get_db)):
    print("user_subscription") #TODO Implementar la función para obtener los canales a los que un usuario está suscrito

def not_subscribed_channels(user_id: int, db: Session = Depends(get_db)):
    print("not_subscribed_channels") #TODO Implementar la función para obtener los canales a los que un usuario no está suscrito

def posts_by_channel(channel_id: int, db: Session = Depends(get_db)):
    print("posts_by_channel") #TODO Implementar la función para obtener los posts de un canal

def create_post(user_id: int , post: schemas.PostBase, db: Session = Depends(get_db)):
    print("create_post") #TODO Implementar la función para crear un post