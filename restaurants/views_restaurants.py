from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Restaurant, MenuItem
from restaurants import app

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(name=request.form['name'],
								   address=request.form['address'],
								   phone=request.form['phone'],
								   website=request.form['website'],
								   cousine=request.form['cousine'],
								   img=request.form['img'])
		session.add(newRestaurant)
		session.commit()
		flash("new restaurant created!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedRestaurant.name = request.form['name']
		if request.form['address']:
			editedRestaurant.address=request.form['address']
		if request.form['phone']:
			editedRestaurant.phone=request.form['phone']
		if request.form['website']:
			editedRestaurant.website=request.form['website']
		if request.form['cousine']:
			editedRestaurant.cousine=request.form['cousine']
		if request.form['img']:
			editedRestaurant.img=request.form['img']
		session.add(editedRestaurant)
		session.commit()
		flash("restaurant edited!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editRestaurant.html', restaurant_id=restaurant_id, item=editedRestaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		session.delete(restaurant)
		session.commit()
		flash("restaurant deleted!")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, item=restaurant)

@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurant=[i.serialize for i in restaurants])


@app.route('/restaurants/<int:restaurant_id>/JSON')
def restaurantJSON(restaurant_id):
    resaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return jsonify(Restaurant=resaurant.serialize)