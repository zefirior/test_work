from functools import partial

from test_work import models as m


def set_default(model, **kw):
    obj = m.db.session.query(model).filter_by(**kw).one_or_none()
    if obj:
        return obj

    obj = model(**kw)
    m.db.session.add(obj)
    m.db.session.flush()
    return obj


ticker_set_default = partial(set_default, m.Ticker)
insider_set_default = partial(set_default, m.Insider)
transaction_type_set_default = partial(set_default, m.TransactionType)


def link_ticker_insider(ticker, insider, row):
    link = m.db.session.query(m.InsiderTicker).filter_by(
        ticker=ticker,
        insider=insider,
    ).one_or_none()
    if link:
        return link

    link = m.InsiderTicker(
        ticker=ticker,
        insider=insider,
        relation=row.relation,
        owner_type=row.owner_type,
    )
    m.db.session.add(link)
    m.db.session.flush()
    return link


def insert_price(ticker, row):
    obj = m.Price(
        ticker=ticker,
        price_date=row.date,
        start=row.start,
        high=row.high,
        low=row.low,
        last=row.last,
        volume=row.volume,
    )
    m.db.session.add(obj)
    m.db.session.flush()
    return obj


def insert_trade(insider_ticker, transaction_type, row):
    obj = m.Trade(
        insider_ticker=insider_ticker,
        transaction_type=transaction_type,
        shares_traded=row.shares_traded,
        last_price=row.last_price,
        shares_held=row.shares_held,
    )
    m.db.session.add(obj)
    # m.db.session.flush()
    return obj
