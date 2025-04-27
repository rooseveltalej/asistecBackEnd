from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db

# Crear una nueva suscripción
def create_subscription(subscription: schemas.SubscriptionBase, db: Session = Depends(get_db)):
    # Verificamos si el usuario ya está suscrito al canal
    existing = db.query(models.Subscription).filter_by(
        user_id=subscription.user_id,
        channel_id=subscription.channel_id
    ).first()
    
    if existing:
        # Si la suscripción existe, verificamos si el estado de is_favorite es diferente
        if existing.is_favorite != subscription.is_favorite:
            # Si es diferente, actualizamos el estado de is_favorite
            existing.is_favorite = subscription.is_favorite
            db.commit()
            db.refresh(existing)
            return JSONResponse(
                content={"msg": "Subscription updated", "subscription_id": existing.subscription_id},
                status_code=status.HTTP_200_OK
            )
        # Si el estado es el mismo, no hacemos nada
        raise HTTPException(status_code=409, detail="User already subscribed with same favorite status")

    # Si no existe la suscripción, creamos una nueva
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

    subscription.is_favorite = False
    db.commit()

    return JSONResponse(
        content={"msg": "SUCCESS"},
        status_code=status.HTTP_200_OK
    )