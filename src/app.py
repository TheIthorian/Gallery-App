from flask import Flask
from flask_cors import CORS, cross_origin

# https://flask-caching.readthedocs.io/en/latest/
# https://www.youtube.com/watch?v=iO0sL6Vyfps
from flask_caching import Cache




app = Flask(__name__)

cache = Cache(app)

CORS(app)

app.config['DEBUG'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CACHE_TYPE'] = 'simple'

