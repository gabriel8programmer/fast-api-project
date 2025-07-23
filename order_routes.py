
from fastapi import APIRouter, Depends

order_router = APIRouter(prefix='/orders', tags=['orders'])
from sqlalchemy.orm import Session
from schemas import OrderSchema
from dependencies import get_session
from models import Order

@order_router.post('/create_order')
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    new_order = Order(user=order_schema.user_id)
    session.add(new_order)
    session.commit()
    return { 'message': f"Pedido criado com sucesso. ID do pedido {new_order.id}" }
