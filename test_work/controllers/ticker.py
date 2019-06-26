from test_work import models as m


def get_tickers():
    tickers = m.db.session.query(m.Ticker).all()
    return dict(result=[t.marshall() for t in tickers])
