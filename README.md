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

```

4. Check [url](http://localhost:5000).

....
## Migration-usecase
0) Start and connect to test server
    ```bash
    docker-compose up -d test
    docker-compose exec test bash
    ```
....
   Next commands execute in this shell - in this `test`-container
....
1) Refesh your local DB according structure in project

    ```bash
    flask db upgrade
    ```

2) Change DB-structure in `thupoll/models.py`

3) Autogenerate migration
    ```bash
    flask db migrate
    ```

4) Migrate local DB:

    ```bash
    flask db upgrade
    ```

