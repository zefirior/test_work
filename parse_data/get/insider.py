import requests
from collections import namedtuple
from bs4 import BeautifulSoup

from parse_data import converters as conv

Meta = namedtuple("Meta", ["name", "converter"])

columns = [
    Meta("insider", str),
    Meta("relation", str),
    Meta("last_date", conv.date_value),
    Meta("tr_type", str),
    Meta("owner_type", str),
    Meta("shares_traded", conv.sum_value),
    Meta("last_price", conv.dec_value),
    Meta("shares_held", conv.sum_value),
]

Row = namedtuple("Row", [i.name for i in columns])


def produce_insider_page(ticker):
    resp = requests.get(
        f"https://www.nasdaq.com/symbol/{ticker}/insider-trades"
    )
    soup = BeautifulSoup(resp.text, "html.parser")
    return list(range(1, find_last_page(soup) + 1))


def find_last_page(soup):
    soup = soup.find(id="quotes_content_left_lb_LastPage")
    if soup is None:
        return 1
    href = soup.get("href")
    _, last_page = href.split("page=")
    return int(last_page)


def insider(ticker, page):
    resp = requests.get(
        f"https://www.nasdaq.com/symbol/{ticker}/insider-trades?page={page}"
    )
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find(attrs={"class": "genTable"}).table
    table = table.find_all("tr")[1:]  # remove header

    for row in table:
        yield parse_row(row)


def parse_row(row):
    fields = {}
    for ceil, meta in zip(row.find_all("td"), columns):
        if ceil.string is None:
            fields[meta.name] = None
            continue
        fields[meta.name] = meta.converter(ceil.string.strip())
    return Row(**fields)


if __name__ == "__main__":
    ticker = "cvx"
    for page in produce_insider_page(ticker):
        for row in insider(ticker, page):
            print(row)
