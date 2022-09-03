from flask import Flask
from flask_cors import CORS, cross_origin

# https://flask-caching.readthedocs.io/en/latest/
# https://www.youtube.com/watch?v=iO0sL6Vyfps
# Caching

app = Flask(__name__)


CORS(app)

app.config['DEBUG'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
