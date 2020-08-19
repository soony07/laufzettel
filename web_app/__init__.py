"""
This file avoids cyclic imports within this package 'web_app'!
"""
from flask import Flask
import pathlib as pl
import sys

# --------------------------------------

def create_app():
    """
        Factory function that created the app.
        Allows to create different instances of the app for testing different configurations.
    """

    # create and configure the app
    app = Flask(__name__)

    app.secret_key = '\xfeUcb\xfe\xdcF\xec&\xdd\xcb$'
    # --------------------------------------
    # get all routes from project
    from web_app.home.routes import home
    from web_app.getbarcode.routes import getbarcode
    from web_app.blankoformular.routes import blankoformular   

    

    # register all routes at app
    app.register_blueprint(home)
    app.register_blueprint(getbarcode)
    app.register_blueprint(blankoformular)

    # todo: deactivate in prod
    app.debug = True

    return app
