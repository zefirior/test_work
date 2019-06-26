import requests
from collections import namedtuple
from bs4 import BeautifulSoup

from parse_data import converters as conv

Meta = namedtuple("Meta", ["name", "converter"])

columns = [
    Meta("date", conv.date_value),
    Meta("start", conv.dec_value),
    Meta("high", conv.dec_value),
    Meta("low", conv.dec_value),
    Meta("last", conv.dec_value),
    Meta("volume", conv.sum_value),
]

Row = namedtuple("Row", [i.name for i in columns])


def historical(ticker):
    url = f"https://www.nasdaq.com/symbol/{ticker}/historical"
    resp = requests.get(url)
    print("request ended")
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find(
        id="historicalContainer").find_all("tr")[1:]  # remove header

    for row in table:
        yield parse_row(row)


def parse_row(row):
    fields = {}
    for ceil, meta in zip(row.find_all("td"), columns):
        fields[meta.name] = meta.converter(ceil.string.strip())
    return Row(**fields)


if __name__ == "__main__":
    for row in historical("cvx"):
        print(row)
