from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db

# Crear una nueva suscripción
def create_subscription(subscription: schemas.SubscriptionBase, db: Session = Depends(get_db)):
    existing = db.query(models.Subscription).filter_by(
        user_id=subscription.user_id,
        channel_id=subscription.channel_id
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="User already subscribed to this channel")

    new_sub = models.Subscription(**subscription.model_dump())
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)
    return JSONResponse(
        content={"msg": "SUCCESS", "subscription_id": new_sub.subscription_id},
        status_code=status.HTTP_201_CREATED
    )

# Eliminar una suscripción existente
def delete_subscription(user_id: int, channel_id: int, db: Session = Depends(get_db)):
    subscription = db.query(models.Subscription).filter_by(
        user_id=user_id,
        channel_id=channel_id
    ).first()

    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )

    db.delete(subscription)
    db.commit()

    return JSONResponse(
        content={"msg": "SUCCESS"},
        status_code=status.HTTP_200_OK
    )