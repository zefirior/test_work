ThuPoll


## Installation

1. Install docker
2. pip install -r requirement.txt


## Run server locally

1. Run db

```bash
docker-compose up -d
```

2. Migrate 

```bash
FLASK_APP=test_work.app_factory:init_app flask db upgrade
```

3. Parse data

```bash
PYTHONPATH=$PYTHONPATH:./ python ./parse_data/parse.py --runner 8 --ticker_file ./tickers.txt
```

4. Up application

```bash
FLASK_APP=test_work.app_factory:init_app flask run
```

5. Check [url](http://localhost:5000).
