from flask import Flask
from flask_migrate import Migrate

from test_work.models import db
from test_work.route import route
from test_work.settings import env
from test_work.utils import CustomJSONEncoder


def init_app(db_url=env.db_url):
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SERVER_NAME'] = env.server_name

    app.app_context().push()
    Migrate(app, db)
    db.app = app
    db.init_app(app)

    route(app)

    return app
