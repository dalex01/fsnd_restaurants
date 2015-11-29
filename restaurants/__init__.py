from flask import Flask

app = Flask(__name__)

import restaurants.views_restaurants
import restaurants.views_menuitems