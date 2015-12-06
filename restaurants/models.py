"""
This file provide DB structure of the application
"""
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    """
    User DB table
    Fields:
        id: user id (primary key)
        name: user name
        email: user email
        img: user image
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    email = Column(String(80), nullable = False)
    img = Column(String(250))

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

class Restaurant(Base):
    """
    Restaurant DB table
    Fields:
        id: restaurant id (primary key)
        name: restaurant name
        address: restaurant address
        phone: restaurant phone
        website: restaurant website
        cousine: restaurant cousine
        img: restaurant img
        user_id: user id who create this restaurant (foreign key: table - User, field - id )
    """
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    address =  Column(String(250))
    phone = Column(String(20))
    website = Column(String(120))
    cousine = Column(String(120))
    img = Column(String(250))
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)
    menuItems = relationship("MenuItem", cascade="all, delete-orphan")

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
    """
    Menu Item DB table
    Fields:
        id: menu item id (primary key)
        name: menu item name
        description: menu item description
        price: menu item price
        course: menu item course
        restaurant_id: restaurant id for which this menu item belongs (foreign key: table - Restaurant, field - id)
        img: menu item img
        user_id: user id who create this menu item (foreign key: table - User, field - id)
    """
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    description = Column(String(500))
    price = Column(String(8))
    course = Column(String(250))
    img = Column(String(250))
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

#engine = create_engine('sqlite:///restaurantmenu.db')
engine = create_engine('postgres://oayymjoacnwrzl:6z1aa9scW0slIYh-B_V5VKGKc-@ec2-46-137-72-123.eu-west-1.compute.amazonaws.com:5432/d1ve6bgi7vcigp')
Base.metadata.create_all(engine)