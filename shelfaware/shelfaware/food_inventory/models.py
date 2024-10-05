from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Text, BLOB
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    lists = relationship('List', back_populates='user')
    actions = relationship('Action', back_populates='user')

class List(Base):
    __tablename__ = 'lists'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    list_items = relationship('ListItem', back_populates='list')
    
    user = relationship('User', back_populates='lists')

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    list_items = relationship('ListItem', back_populates='category')

class FoodItem(Base):
    __tablename__ = 'food_items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    barcode = Column(String, nullable=True)
    image = Column(BLOB, nullable=True)
    description = Column(Text, nullable=True)

class ListItem(Base):
    __tablename__ = 'list_items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    quantity = Column(Float, nullable=False, default=1.0)
    date_added = Column(DateTime, default=datetime.datetime.utcnow)
    date_removed = Column(DateTime, nullable=True)
    list_id = Column(Integer, ForeignKey('lists.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    food_id = Column(Integer, ForeignKey('food_items.id'), nullable=True)  # Link to FoodItem
    
    list = relationship('List', back_populates='list_items')
    category = relationship('Category', back_populates='list_items')
    food = relationship('FoodItem')

class Action(Base):
    __tablename__ = 'actions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    action_type = Column(String, nullable=False)  # e.g., "purchase", "remove", "consume"
    quantity = Column(Float, nullable=False, default=1.0)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    list_item_id = Column(Integer, ForeignKey('list_items.id'), nullable=True)  # Link to ListItem
    
    user = relationship('User', back_populates='actions')
    list_item = relationship('ListItem')

def get_engine():
    engine = create_engine('sqlite:///food_inventory.db')
    return engine

def create_tables(engine):
    Base.metadata.create_all(engine)
