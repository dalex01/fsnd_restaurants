from flask import Flask, render_template, url_for, jsonify, make_response
from restaurants.helpers import dbConnect
from models import Base, Restaurant, MenuItem
from restaurants import app



session = dbConnect()


@app.route('/restaurants/JSON')
def restaurantsJSON():
    """
    Create JSON endpoint for all restaurants
    """
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurant=[i.serialize for i in restaurants])


@app.route('/restaurant/<int:restaurant_id>/JSON')
def restaurantJSON(restaurant_id):
    """
    Create JSON endpoint for particular restaurant
    Input:
        restaurant_id - restaurant's ID for which we want to display endpoint
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return jsonify(Restaurant=restaurant.serialize)


@app.route('/restaurants/XML')
def restaurantsXML():
    """
    Create XML endpoint for all restaurants
    """
    restaurants = session.query(Restaurant).all()
    xml = render_template('restaurants.xml', restaurants=restaurants)
    response = make_response(xml)
    response.headers["Content-Type"] = "application/xml"
    return response


@app.route('/restaurant/<int:restaurant_id>/XML')
def restaurantXML(restaurant_id):
    """
    Create XML endpoint for particular restaurant
    Input:
        restaurant_id - restaurant's ID for which we want to display endpoint
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    xml = render_template('restaurant.xml', restaurant=restaurant)
    response = make_response(xml)
    response.headers["Content-Type"] = "application/xml"
    return response


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    """
    Create JSON endpoint for particular Menu
    Input:
        restaurant_id - restaurant's ID for which menu we want to display endpoint
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    """
    Create JSON endpoint for particular menu item
    Input:
        restaurant_id - restaurant's ID for which we want to display endpoint
        menu_id - menu item id to display
    """
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=item.serialize)

@app.route('/restaurant/<int:restaurant_id>/menu/XML')
def restaurantMenuXML(restaurant_id):
    """
    Create XML endpoint for particular Menu
    Input:
        restaurant_id - restaurant's ID for which menu we want to display endpoint
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    xml = render_template('menu.xml', restaurant_id=restaurant_id, items=items)
    response = make_response(xml)
    response.headers["Content-Type"] = "application/xml"
    return response


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/XML')
def menuItemXML(restaurant_id, menu_id):
    """
    Create XML endpoint for particular menu item
    Input:
        restaurant_id - restaurant's ID for which we want to display endpoint
        menu_id - menu item id to display
    """
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    xml = render_template('menuItem.xml', restaurant_id=restaurant_id, item=item)
    response = make_response(xml)
    response.headers["Content-Type"] = "application/xml"
    return response