"""
This file provide all application helper functions
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Restaurant, MenuItem, User
from functools import wraps
from flask import g, request, redirect, url_for
from flask import session as login_session

def dbConnect():
	"""
	Connect to DB and create session
	"""
	#engine = create_engine('sqlite:///restaurantmenu.db')
	engine = create_engine('postgres://oayymjoacnwrzl:6z1aa9scW0slIYh-B_V5VKGKc-@ec2-46-137-72-123.eu-west-1.compute.amazonaws.com:5432/d1ve6bgi7vcigp')
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	return session

session = dbConnect()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect(url_for('showLogin'))
        return f(*args, **kwargs)
    return decorated_function


def createUser(login_session):
    """
    Create a new user based on information from current session
    Input:
        login_session - dictionary with current user information
    Output:
        User ID.
    """
    newUser = User(name=login_session['username'], email=login_session['email'], img=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """
    Get user information from DB based on user ID
    Input:
        user_id - user ID
    Output:
        Object of User class.
    """
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """
    Get user ID form DB based on user email
    Input:
        email - user email
    Output:
        None - if user with provided email is not in DB
        user ID - if user with provided email is in DB
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None