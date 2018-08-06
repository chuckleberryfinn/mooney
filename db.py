import psycopg2


class CoinsDatabase(object):
    def __init__(self): 
        self.conn = psycopg2.connect("dbname='mooney'")

    def insert_coins(self, coins):
        curr = self.conn.cursor()
        curr.execute("Create temporary table temp_coins(name varchar(255), ticker varchar(100)) on commit drop")
        curr.executemany("Insert into temp_coins(name, ticker) values (%(name)s, %(ticker)s) ", coins)
        curr.execute("Insert into coins(name, ticker) select tc.name, tc.ticker from temp_coins tc left join coins c using(name) where c.name is null")
        self.conn.commit()

    def coin_ids(self):
        curr = self.conn.cursor()
        curr.execute("select coin_id, name from coins")
        return curr.fetchall()

    def insert_prices(self, prices):
        curr = self.conn.cursor()
        curr.executemany("Insert into prices(coin_id, euro, dollar) values (%(coin_id)s, %(euro)s, %(dollar)s)", prices)
        self.conn.commit()

    def get_coins(self):
        curr = self.conn.cursor()
        curr.execute("Select name, ticker from coins")
        return {r[0]:r[1] for r in curr.fetchall()}

    def get_latest_price(self, coin):
        curr = self.conn.cursor()
        curr.execute("""with daily_prices as (
                            select * from prices
                            join coins using(coin_id)
                            where time >= (select max(time::date) from prices)
                            and name = (%s)
                            order by time asc
                        ),
                        min_max_prices as (
                            select name, max(euro), min(euro)
                            from daily_prices
                            group by name
                        ),
                        all_prices as (
                            select row_number() over (partition by name order by time desc)
                            rn, name, ticker, euro, dollar, time
                            from daily_prices
                        ),
                        median_prices as (
                            select name, median(euro) as median
                            from all_prices
                            group by name
                        ),
                        latest_prices as (
                            select name, ticker, euro, dollar
                            from all_prices
                            where rn = 1
                        ),
                        first_price as (
                            select name, euro from daily_prices
                            where name=(%s)
                            limit 1
                        )
                        select name, ticker, lp.euro, dollar, min, max,
                        ((lp.euro - fp.euro)*100)/fp.euro, median
                        from latest_prices as lp
                        join min_max_prices using(name)
                        join first_price as fp using(name)
                        join median_prices using(name)
                     """, (coin, coin))
        return curr.fetchone()

    def check_ats(self, coin):
        curr = self.conn.cursor()
        curr.execute("""
                        with all_ats as (
                            select min(euro) as lowest, max(euro) as ath
                            from prices
                            join coins using(coin_id)
                            where name = (%s)
                            union select min_euro as lowest, max_euro as ath
                            from daily_stats
                            join coins using(coin_id)
                            where name = (%s)
                        )
                        select min(lowest) as lowest, max(ath) as ath
                        from all_ats
                     """, (coin, coin))
        return curr.fetchone()

    def dated_ats(self, coin):
        curr = self.conn.cursor()
        curr.execute("""
                        with all_ats as (
                            select min(euro) as lowest, max(euro) as ath
                            from prices
                            join coins using(coin_id)
                            where name = (%s)
                            union select min_euro as lowest, max_euro as ath
                            from daily_stats
                            join coins using(coin_id)
                            where name = (%s)
                        ),
                        extremes as (
                            select min(lowest) as minimum, max(ath) as ath
                            from all_ats
                        ),
                        lowest as (
                            select time::date as date, euro as price
                            from prices
                            join coins using(coin_id)
                            where euro=(select minimum from extremes)
                            and name = (%s)
                            union select date, min_euro as price
                            from daily_stats
                            join coins using(coin_id)
                            where min_euro=(select minimum from extremes)
                            and name = (%s)
                            limit 1
                        ),
                        highest as (
                            select time::date as date, euro as price
                            from prices
                            join coins using(coin_id)
                            where euro=(select ath from extremes)
                            and name = (%s)
                            union select date, max_euro as price
                            from daily_stats
                            join coins using(coin_id)
                            where max_euro=(select ath from extremes)
                            and name = (%s)
                            limit 1
                        )

                        select date, price from lowest union select date, price from highest
                        order by price asc;
                     """, (coin, coin, coin, coin, coin, coin))
        return curr.fetchall()

    def get_stats(self, coin, date):
        curr = self.conn.cursor()
        curr.execute("""
                        select name, ticker, date, min_euro, average_euro, median_euro, std_dev, max_euro
                        from daily_stats
                        join coins using(coin_id)
                        where name = (%s)
                        and date = (%s)
                      """, (coin, date))
        return curr.fetchone()

    def get_movers(self, sort='desc'):
        curr = self.conn.cursor()
        curr.execute("""
                        with movers as (
                            select distinct coin_id, first_value(euro) over w as first, last_value(euro) over w as last
                            from prices where time::date=current_date WINDOW w as (
                                partition by coin_id order by time range between unbounded preceding and unbounded
                                following) order by coin_id
                        )
                        select name, ticker, first, last, (last-first)*100/first as diff
                        from movers
                        join coins using(coin_id)
                        order by diff %s limit 3;
                    """ % sort)
        return curr.fetchall()

    def gen_stats(self):
        curr = self.conn.cursor()
        curr.execute("""
                        truncate daily_stats;
                        insert into daily_stats(coin_id, date, min_euro, average_euro, median_euro, std_dev, max_euro) (
                        select coin_id, time::date, min(euro), avg(euro), median(euro), stddev_pop(euro), max(euro)
                        from prices group by coin_id, time::date);
                    """)

    def get_advice(self):
        curr = self.conn.cursor()
        curr.execute("""
                        select response from advice offset floor(random()*(select count(*) from advice)) limit 1;
                     """)
        return curr.fetchone()

    def get_remark(self, comment):
        curr = self.conn.cursor()
        curr.execute("""
                        with all_remarks as (
                            select remark from replies
                            join replies_remarks using(reply_id)
                            join remarks using(remark_id)
                            where %s ~ regex
                        )
                        select * from all_remarks
                        offset floor(random() * (select count(*) from all_remarks))
                        limit 1;
                     """, (comment,))
        return curr.fetchone()

    def is_admin(self, user):
        curr = self.conn.cursor()
        curr.execute("""
                        select 1 from users
                        where username = %s
                        and administrator is True
                     """, (user,))
        return curr.fetchone()


if __name__ == '__main__':
    pass
