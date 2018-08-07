# -*- coding: utf-8 -*-
import logging

from datetime import date, timedelta

import coins
import replies


logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.INFO)


class Price(object):
    def __init__(self, coin):
        self.coin = coins.Coin(coin)

    def get_response(self):
        return '%s' % self.coin.price()


class Ats(object):
    def __init__(self, coin):
        self.coin = coins.ATS(coin)

    def get_response(self):
        low_date, low, high_date, high = self.coin.raw_ats()
      
        return 'All Time \x0305Low\x03/\x0303High\x03 Prices for {}, Lowest: \x0305€{:,}\x03 on {} Highest: \x0303€{:,}\x03 on {}'\
                .format(self.coin._price()['Name'], low, low_date, high, high_date)


class Stats(object):
    def __init__(self, coin, date=date.today() - timedelta(days=1)):
        self.coin = coins.Stats(coin)
        self.date = date

    def get_response(self):
        return '%s' % self.coin.stats(self.date)


class Advice(object):
    def get_response(self):
        return replies.Advice().response()


class Alert(object):
    def __init__(self):
        self.coin = coins.ATS()

    def get_response(self, coin):
        return self.coin.ats()


class Auto(object):
    def get_response(self, comment):
        return replies.Auto().response(comment)


class Targeted(object):
    def __init__(self, sender):
        self.sender = sender

    def get_response(self, comment):
        return replies.Targeted(self.sender).response(comment)


class Admin(object):
    def __init__(self, sender):
        self.sender = sender

    def get_response(self):
        return replies.Admin().response(self.sender)


class Bulls(object):
    def __init__(self):
        self.coins = coins.Coins()

    def get_response(self):
        return self.coins.bulls()


class Bears(object):
    def __init__(self):
        self.coins = coins.Coins()

    def get_response(self):
        return self.coins.bears()


class Fiat(object):
    def __init__(self, coin, amount=1):
        self.coin = coins.Coin(coin)
        self.amount = amount

    def get_response(self):
        return self.coin.converter(self.amount)


class Diff(object):
    def __init__(self, coin, date):
        self.coin = coins.Coin(coin)
        self.date = date

    def get_response(self):
        return 'Diff'


if __name__ == '__main__':
    pass
