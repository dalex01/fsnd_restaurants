from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Restaurant, MenuItem
from restaurants import app

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/')
def restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurants/new/')
def newRestaurantItem():
    return render_template('newrestaurantitem.html')

@app.route('/restaurants/<int:restaurant_id>/edit/')
def editRestaurantItem(restaurant_id):
    return render_template('editrestaurantitem.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/delete/')
def deleteRestaurantItem(restaurant_id):
    return render_template('deleterestaurantitem.html', restaurant_id=restaurant_id)