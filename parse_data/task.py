from threading import RLock

from parse_data import get
from parse_data import queries as q
from test_work.models import db


def produce_page_task(manager, code):
    def task():
        lock = RLock()
        for page in get.produce_insider_page(code)[:10]:
            manager.queue.append(insider_task(code, page, lock))
        print(f"For ticker {code} will be parse insider info in pages:1-{page}")
    return task


def insider_task(code, page, lock):
    def task():
        print(f"Parse insider info for ticket {code} (page: {page})")

        data = list(get.insider(code, page))

        with lock:
            ticker = q.ticker_set_default(code=code)
            for row in data:
                tr_type = q.transaction_type_set_default(code=row.tr_type)
                insider = q.insider_set_default(name=row.insider)
                link = q.link_ticker_insider(ticker, insider, row)
                q.insert_trade(link, tr_type, row)
            db.session.commit()

    return task


def historical_task(code):
    def task():
        print(f"Parse history for ticket {code}")
        ticker = q.ticker_set_default(code=code)
        data = list(get.historical(code))

        for row in data:
            q.insert_price(ticker, row)

        db.session.commit()
    return task
