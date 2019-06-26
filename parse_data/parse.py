import click
from threading import RLock
from sqlalchemy.exc import InvalidRequestError, IntegrityError, OperationalError

from parse_data import get, Manager
from parse_data import queries as q
from test_work.app_factory import init_app
from test_work.models import db


RETRY_NUM = 8


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


def clear_db():
    for table in db.metadata.tables:
        db.engine.execute('TRUNCATE TABLE {} CASCADE'.format(table))


@click.command()
@click.option('--runner', "-r", default=1, help='Number of runners.')
@click.option('--ticker_file', "-p", type=click.File(), help='Path to file with tickers.')
def parse(runner, ticker_file):
    init_app()
    clear_db()
    m = Manager(runner)
    for ticket in ticker_file:
        ticket = ticket.strip()
        m.queue.append(historical_task(ticket))
        m.queue.append(produce_page_task(m, ticket))
    m.run()


if __name__ == "__main__":
    parse()
