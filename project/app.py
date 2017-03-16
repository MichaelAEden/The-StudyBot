from flask_flatpages import FlatPages
from flask_frozen import Freezer
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('settings.py')
pages = FlatPages(app)
freezer = Freezer(app)