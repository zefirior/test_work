from flask import Blueprint, render_template
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
from test_work.utils import date_field, strptime_or_none

blue = Blueprint("root", __name__)


@blue.route("/")
def tickers():
    tickers = get_tickers()

    return render_template("tickers.html", tickers=tickers)


@blue.route("/<ticker>/")
def price(ticker):
    prices = get_price(ticker)
    return render_template("price.html", prices=prices, ticker=ticker)


@blue.route("/<ticker>/insider/")
def insider(ticker):
    insiders = get_insider(ticker)
    return render_template("insiders.html", insiders=insiders, ticker=ticker)


@blue.route("/<ticker>/insider/<int:insider_id>")
def trades(ticker, insider_id):
    trades = get_trade(ticker, insider_id)
    return render_template(
        "trade.html",
        trades=trades,
        ticker=ticker,
        insider_id=insider_id,
    )


@blue.route("/<ticker>/analitics/")
@use_kwargs({
    "date_from": date_field,
    "date_to": date_field,
})
def ticker_analitics(ticker, date_from, date_to):
    start = strptime_or_none(date_from)
    end = strptime_or_none(date_to)
    data = get_analitics(ticker, start, end)

    return render_template(
        "analitics.html",
        analitics=data,
        ticker=ticker,
    )


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
    data = get_delta(ticker, value, map_price_column[type])
    return render_template(
        "delta.html",
        data=data,
        ticker=ticker,
    )
