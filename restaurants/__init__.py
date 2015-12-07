from flask import Flask
from flask.ext.seasurf import SeaSurf

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
csrf = SeaSurf(app)

import restaurants.views
