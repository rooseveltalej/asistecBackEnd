from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas
from database import get_db
from controllers.subscription_controllers import  create_subscription, delete_subscription, make_admin


subscription_router = APIRouter(prefix="/api/subscriptions", tags=["Subscriptions"])

# Crear una nueva suscripción
@subscription_router.post("/create_subscription", status_code=status.HTTP_201_CREATED, response_model=dict)
def create_subscription_route(subscription: schemas.SubscriptionBase, db: Session = Depends(get_db)):
    return create_subscription(subscription, db)

# Eliminar una suscripción
@subscription_router.delete("/delete_subscription", response_model=dict)
def delete_subscription_route(user_id: int, channel_id: int, db: Session = Depends(get_db)):
    return delete_subscription(user_id, channel_id, db)

# Asignar privilegios de administrador a un usuario en un canal
@subscription_router.put("/make_admin", response_model=dict, status_code=status.HTTP_200_OK)
def make_admin_route(user_id: int, channel_id: int, db: Session = Depends(get_db)):
    return make_admin(user_id, channel_id, db)
