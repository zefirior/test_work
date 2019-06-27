from flask import Flask

from test_work.blueprints.api import blue as api
from test_work.blueprints.root import blue as root


def hello():
    return "Hello"


def route(app: Flask):
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(root, url_prefix="/")
