from test_work import models as m


def delta(ticker, limit, price_type):
    conn = m.db.engine.connect()

    conn.execute(
        sum_diff_stmt.format(price_type=price_type),
        ticker,
    )

    result = conn.execute(select_stmt, limit)
    result = result.fetchone()
    conn.close()
    m.db.engine.dispose()

    if not result:
        return {}

    return dict(result)


sum_diff_stmt = """
    create temporary table tt_sum_diff as
        with pre_calc as (
            select
                p.id,
                p.price_date as date_from,
                lag(p.price_date, -1) OVER(ORDER BY p.price_date) as date_to,
                abs(lag(p.{price_type}, -1) OVER(ORDER BY p.price_date) - p.{price_type}) as diff
            from ticker t
                join price p on t.id = p.ticker_id
            where t.code = %s
            order by p.price_date
      )

      select
            id,
            date_from,
            date_to,
            diff,
            sum(diff) over (ORDER BY date_from) - diff as from_sum,
            sum(diff) over (ORDER BY date_from) as to_sum
        from pre_calc
        where date_to is not null
        order by date_from;
"""

select_stmt = """
    select
           d1.date_from,
           d2.date_to,
           d2.date_to - d1.date_from as date_diff,
           d1.from_sum,
           d2.to_sum,
           d2.to_sum - d1.from_sum as diff
    from
        tt_sum_diff d1
            join
        tt_sum_diff d2 on d2.date_to > d1.date_from
    where d2.to_sum - d1.from_sum > %s
    order by d2.date_to - d1.date_from, d1.date_from
    limit 1;
"""
