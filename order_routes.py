
from fastapi import APIRouter

order_router = APIRouter(prefix='/orders', tags=['orders'])

@order_router.get('/')
async def list_orders ():
    '''Lista os pedidos. Requer autenticação de usuário'''
    return { 'message': 'Hello world!' }
