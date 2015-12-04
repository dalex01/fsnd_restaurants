import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    address =  Column(String(250))
    phone = Column(String(20))
    website = Column(String(120))
    cousine = Column(String(120))
    img = Column(String(120))
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    # We added this serialize function to be able to send JSON objects in a
    # serializable format
    @property
    def serialize(self):

        return {
            'name': self.name,
            'address': self.address,
            'id': self.id,
            'phone': self.phone,
            'website': self.website,
            'cousine': self.cousine,
            'img': self.img
        }

class MenuItem(Base):
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    img = Column(String(120))
    restaurant_id = Column(Integer,ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    # We added this serialize function to be able to send JSON objects in a
    # serializable format
    @property
    def serialize(self):

        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
            'img': self.img
        }

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    email = Column(String(80), nullable = False)
    img = Column(String(120))

    # We added this serialize function to be able to send JSON objects in a
    # serializable format
    @property
    def serialize(self):

        return {
            'name': self.name,
            'email': self.email,
            'id': self.id,
            'img': self.img
        }

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)