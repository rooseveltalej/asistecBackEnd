from fastapi import Depends, HTTPException
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
        raise HTTPException(status_code=400, detail="User already subscribed to this channel")

    new_sub = models.Subscription(**subscription.model_dump())
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)
    return {"msg": "SUCCESS", "subscription_id": new_sub.subscription_id}

# Eliminar una suscripción existente
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    subscription = db.query(models.Subscription).filter_by(subscription_id=subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    db.delete(subscription)
    db.commit()
    return {"msg": "SUCCESS"}