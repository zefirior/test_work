from flask import Blueprint, jsonify
from webargs import fields, validate
from webargs.flaskparser import use_kwargs

from test_work.controllers.ticker import (
    get_tickers,
    get_price,
    get_insider,
    get_trade,
    get_analitics
)
from test_work.controllers.delta import get_delta
from test_work.utils import CustomJSONEncoder, date_field, strptime_or_none

blue = Blueprint("api", __name__)
blue.json_encoder = CustomJSONEncoder


@blue.route("/")
def tickers():
    return jsonify(result=get_tickers())


@blue.route("/<ticker>/")
def price(ticker):
    return jsonify(result=get_price(ticker))


@blue.route("/<ticker>/insider/")
def insider(ticker):
    return jsonify(result=get_insider(ticker))


@blue.route("/<ticker>/insider/<int:insider_id>")
def trade(ticker, insider_id):
    return jsonify(result=get_trade(ticker, insider_id))


@blue.route("/<ticker>/analitics/")
@use_kwargs({
    "date_from": date_field,
    "date_to": date_field,
})
def ticker_analitics(ticker, date_from, date_to):
    start = strptime_or_none(date_from)
    end = strptime_or_none(date_to)
    return jsonify(result=get_analitics(ticker, start, end))


map_price_column = {
    "open": "start",
    "high": "high",
    "low": "low",
    "close": "last",
}


@blue.route("/<ticker>/delta/")
@use_kwargs({
    "value": fields.Decimal(required=True),
    "type": fields.Str(
        required=True,
        validate=validate.OneOf(list(map_price_column)),
    ),
})
def ticker_delta(ticker, value, type):
    result = get_delta(ticker, value, map_price_column[type])
    return jsonify(request=result)
