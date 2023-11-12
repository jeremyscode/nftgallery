# Import the Flask basics
from flask import Flask, flash, redirect, url_for
from flask_bootstrap import Bootstrap
import logging


# Define the App
app = Flask(__name__)
app.config.from_pyfile('../config.py')

Bootstrap(app)

#
# Module Imports
#

# Import the module / component using their blueprints
from nftgallery.home.views import home

# Register Blueprints
app.register_blueprint(home)

# Flask module stuff
@app.after_request
def add_header(response):
    """ added for auth issue where users are logged in
     and seeing other users profiles """
    response.cache_control.private = True
    response.cache_control.public = False
    return response
