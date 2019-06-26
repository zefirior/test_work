from flask import Flask

from test_work.blueprints.api import blue

def hello():
    return "Hello"


def route(app: Flask):
    app.register_blueprint(blue, url_prefix="/api")
    app.route("/")(hello)
