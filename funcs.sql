CREATE TYPE named_value AS (
  from_date date,
  to_date date
);

CREATE FUNCTION pyf1 (ticker varchar, code varchar)
  RETURNS named_value
AS $$
    from datetime import datetime
    # import plpy

    stmt = (
        "select p.price_date, p.{} as value "
        "from price p "
        " join ticker t "
        "   on t.ticker_id = p.ticker_id"
        "where t.code = $1"
        "order by p.price_date"
    ).format(code)

    plan = plpy.prepare(stmt)
    rv = plpy.execute(plan, ticker)
    print(rv[0]["price_date"], rv[0]["value"])
    print(rv[2]["price_date"], rv[4]["value"])
    return (rv[0]["price_date"], rv[1]["price_date"])

$$ LANGUAGE plpythonu;
