from test_work import models as m


def get_tickers():
    tickers = m.db.session.query(m.Ticker).all()
    return [t.marshall() for t in tickers]


def get_ticker(ticker: str):
    return m.db.session.query(m.Ticker).filter_by(code=ticker).one()


def get_price(ticker: str):
    ticker = get_ticker(ticker)
    price = m.db.session.query(m.Price).filter(
        m.Price.ticker == ticker
    ).all()

    return [p.marshall() for p in price]


def get_insider(ticker: str):
    ticker = get_ticker(ticker)
    insider = m.db.session.query(
        m.Insider, m.InsiderTicker
    ).join(
        m.InsiderTicker
    ).filter(
        m.InsiderTicker.ticker == ticker
    ).all()

    result = []
    for insider, it in insider:
        result.append(dict(
            id=insider.id,
            name=insider.name,
            relation=it.relation,
            owner_type=it.owner_type,
        ))

    return result


def get_trade(ticker: str, insider_id):
    ticker = get_ticker(ticker)
    trades = m.db.session.query(
        m.Trade
    ).join(
        m.InsiderTicker
    ).filter(
        m.InsiderTicker.ticker == ticker,
        m.InsiderTicker.insider_id == insider_id,
    ).all()

    result = []
    for trade in trades:
        result.append(trade.marshall())

    return result


def get_price_for_date(ticker: str, price_date):
    ticker = get_ticker(ticker)

    return m.db.session.query(m.Price).filter(
        m.Price.ticker == ticker,
        m.Price.price_date == price_date
    ).one_or_none()


def analitics(ticker: str, start, end):
    start = get_price_for_date(ticker, start)
    end = get_price_for_date(ticker, end)

    if start and end:
        return dict(
            start=end.start - start.start,
            high=end.high - start.high,
            low=end.low - start.low,
            last=end.last - start.last,
        )
    return {}
