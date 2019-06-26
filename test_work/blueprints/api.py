import json
from flask import Blueprint

from test_work.controllers.ticker import get_tickers

blue = Blueprint("api", __name__)


@blue.route("/")
def tickers():
    return json.dumps(get_tickers())
