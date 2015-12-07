"""
This file provide all routes of the application
"""
# Import all necessary modules
from flask import Flask, render_template, url_for, redirect, request, flash, jsonify, make_response
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from models import Base, Restaurant, MenuItem, User
from restaurants import app
from restaurants.helpers import dbConnect, createUser, getUserID, getUserInfo, login_required
import httplib2, json, requests, random, string, os

session = dbConnect()


@app.route('/login')
def showLogin():
    """
    Login page
    Output:
        Rendered login page
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """
    Facebook connect page
    Output:
        output of Facebook login attempt depending on login status
    """
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    app_id = json.loads(open(os.path.join(os.path.dirname(__file__), "instance/fb_client_secrets.json"), 'r').read())['web']['app_id']
    app_secret = json.loads(open(os.path.join(os.path.dirname(__file__), "instance/fb_client_secrets.json"), 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    """
    Logout if was logged in using Facebook account
    """
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Google connect page
    Output:
        output of Google login attempt depending on login status
    """
    CLIENT_ID = json.loads(open(os.path.join(os.path.dirname(__file__), "instance/client_secrets.json"), 'r').read())['web']['client_id']
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(os.path.join(os.path.dirname(__file__), 'instance/client_secrets.json'), scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    user_id = getUserID(login_session['email'])
    if user_id is None:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """
    Logout if was logged in using Google account
    """
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    """
    Main logout function which:
        call Google or Facebook logout depending on login method
        clear all current session information
    """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showRestaurants'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showRestaurants'))


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    """
    All restaurants page
    Output:
        Rendered restaurants page
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    restaurants = session.query(Restaurant).all()
    # Render public template if user is not logged in
    if 'username' not in login_session:
        return render_template('publicrestaurants.html', restaurants = restaurants, STATE=state)
    # Render normal template if user logged in
    else:
        return render_template('restaurants.html', restaurants = restaurants)


@app.route('/restaurant/new/', methods=['GET', 'POST'])
@login_required
def newRestaurant():
    """
    New restaurant page
    Output:
        Render new restaurant creation page or populate entered info into DB and redirect to all restaurants page
    """
    # Redirect to login page if user is not logged in
    #if 'username' not in login_session:
    #    return redirect('/login')
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
@login_required
def editRestaurant(restaurant_id):
    """
    Edit restaurant info page
    Input:
        restaurant_id - restaurant id to edit
    Output:
        Render edit restaurant page or update entered info into DB and redirect to all restaurants page
    """
    # Redirect to login page if user is not logged in
    #if 'username' not in login_session:
    #    return redirect('/login')
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    # Alert if logged in user doesn't have permission to edit restaurant (restaurant was created by some other user)
    if editedRestaurant.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this restaurant. \
                Please create your own restaurant in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        # Check if particular field was changed
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
@login_required
def deleteRestaurant(restaurant_id):
    """
    Delete restaurant info page
    Input:
        restaurant_id - restaurant id to delete
    Output:
        Render delete restaurant page or delete restaurant and redirect to all restaurants page
    """
    # Redirect to login page if user is not logged in
    #if 'username' not in login_session:
    #    return redirect('/login')
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    # Alert if logged in user doesn't have permission to delete restaurant (restaurant was created by some other user)
    if restaurant.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this restaurant. \
                Please create your own restaurant in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash("restaurant deleted!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, item=restaurant)


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


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    """
    Menu page for particular restaurant
    Input:
        restaurant_id - restaurant id for which we want to render menu
    Output:
        Rendered restaurants page
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    creator = getUserInfo(restaurant.user_id)
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    # Render public template if user is not logged in or restaurant was created by some other user
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicmenu.html', restaurant = restaurant, items = items, creator=creator, STATE=state)
    # Render normal template otherwise
    else:
        return render_template('menu.html', restaurant = restaurant, items = items, creator=creator)


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
@login_required
def newMenuItem(restaurant_id):
    """
    New menu item page
    Input:
        restaurant_id - restaurant id for which we want to create new menu item
    Output:
        Render new menu item creation page or populate entered info into DB and redirect to this restaurant's menu page
    """
    # Redirect to login page if user is not logged in
    #if 'username' not in login_session:
    #    return redirect('/login')
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'],
                           description=request.form['description'],
                           price=request.form['price'],
                           course=request.form['course'],
                           img=request.form['img'],
                           restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
@login_required
def editMenuItem(restaurant_id, menu_id):
    """
    Edit menu item info page
    Input:
        restaurant_id - restaurant id which menu item we want to edit
        menu_id - menu item id to edit
    Output:
        Render edit menu item page or update entered info into DB and redirect to this restaurant's menu page
    """
    # Redirect to login page if user is not logged in
    #if 'username' not in login_session:
    #    return redirect('/login')
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    # Alert if logged in user doesn't have permission to edit menu item (menu item was created by some other user)
    if editedItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this menu item. \
                Please create your own in order to edit.');}</script><body onload='myFunction()''>"
    # Check if particular field was changed
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description=request.form['description']
        if request.form['price']:
            editedItem.price=request.form['price']
        if request.form['course']:
            editedItem.course=request.form['course']
        if request.form['img']:
            editedItem.img=request.form['img']
        session.add(editedItem)
        session.commit()
        flash("menu item edited!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteMenuItem(restaurant_id, menu_id):
    """
    Delete menu item info page
    Input:
        restaurant_id - restaurant id which menu item we want to delete
        menu_id - menu item id to delete
    Output:
        Render delete menu item page or delete menu item and redirect to this restaurant's menu page
    """
    # Redirect to login page if user is not logged in
    #if 'username' not in login_session:
    #    return redirect('/login')
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    # Alert if logged in user doesn't have permission to delete menu item (menu item was created by some other user)
    if item.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this menu item. \
                Please create your own in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("menu item deleted!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', item=item, restaurant_id=restaurant_id)


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