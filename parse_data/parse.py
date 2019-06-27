import click

from parse_data import Manager
from parse_data.task import historical_task, produce_page_task
from test_work.app_factory import init_app
from test_work.models import db


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
