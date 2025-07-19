
from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import ChoiceType

# cria o banco de dados
db = create_engine('sqlite:///banco.db')

# cria a base do banco de dados
Base = declarative_base()

# cria as tabelas do bancos
class User(Base):
    __tablename__ = 'users'
    
    id=Column('id', Integer, primary_key=True, autoincrement=True)
    name=Column('name', String)
    email=Column('email', String, nullable=False)
    password=Column('password', String)
    actived=Column('actived', Boolean)
    admin=Column('admin', Boolean, default=False)
    
    def __init__(self, name, email, password, actived=True, admin=False):
        self.name = name
        self.email =email
        self.password= password
        self.actived = actived
        self.admin = admin

class Order(Base):
    __tablename__='orders'
    
    order_types = (
        ('PENDENTE', 'PENDENTE'),
        ('CANCELADO', 'CANCELADO'),
        ('FINALIZADO', 'FINALIZADO')
    )
    
    id=Column('id', Integer, primary_key=True, autoincrement=True)
    status=Column('status', ChoiceType(choices=order_types)) #pendente #cancelado #finalizado
    user=Column('user', String, ForeignKey('users.id'))
    price=Column('price', Float)
    
    def __init__(self, user, status='PENDENTE', price=0):
        self.user = user
        self.status = status
        self.price = price
    
class Order_items(Base):
    __tablename__='order_items'
    
    id=Column('id', Integer, primary_key=True, autoincrement=True)
    amound=Column('amound', Integer)
    flavor=Column('flavor', String)
    size=Column('size', String)
    unit_price=Column('unit_price', Float)
    order=Column('order', ForeignKey('orders.id'))
        
    def __init__(self, amound, flavor, size, unit_price, order):
        self.amound = amound
        self.flavor = flavor
        self.size = size
        self.unit_price= unit_price
        self.order = order

# executa a criação dos metadados do banco 

