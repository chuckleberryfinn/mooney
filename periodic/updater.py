import json
import logging
import psycopg2
import time

from decimal import *
from urllib.request import urlopen, Request

from mooney.db import CoinsDatabase


logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.INFO)


class Coins(object):
    def __init__(self, api_key):
        self.url = 'https://www.worldcoinindex.com/apiservice/json?key=%s' % api_key

    def get_prices(self):
        logging.info('Get updated price')
        req = Request(self.url, headers={ 'User-Agent': 'Mooney/1.0' })
        prices = json.loads(urlopen(req, timeout=10).read().decode())
        return prices


class Coin(object):
    def __init__(self, c):
        self.name = str(c['Name']).title()
        self.nick = str(c['Label'].split('/')[0]).upper()
        self.euro = self.format_price(c['Price_eur'])
        self.dollar = self.format_price(c['Price_usd'])

    @staticmethod
    def format_price(price):
        if price < 1:
            return price
        return Decimal('%.2f' % price)


class Updater(object):
    def __init__(self, prices):
        self.prices = self._prices(prices)
        self.cd = CoinsDatabase()

    def _prices(self, prices):
        return {c['Name'].lower():Coin(c) for c in prices['Markets']}

    def update_prices(self):
        self.add_coins()
        self.add_prices()
        
    def add_coins(self):
        coins = [{'name': c.name.lower(), 'ticker': c.nick.lower()} for c in self.prices.values()]
        self.cd.insert_coins(coins)

    def add_prices(self):
        coin_ids = self.cd.coin_ids()
        self.cd.insert_prices([{'coin_id': cid, 'euro': self.prices[c].euro, 'dollar': self.prices[c].dollar}
                                for cid, c in coin_ids if c in self.prices])


def main():
    while True:
        api_key = open('api.key', 'r').read().strip()
        coins = Coins(api_key)
        prices = coins.get_prices()
        updater = Updater(prices)
        updater.update_prices()
        time.sleep(5*60)


if __name__ == '__main__':
    while True:
        try:
            main()
        except:
            logging.exception("")
        time.sleep(60)
