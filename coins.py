# -*- coding: utf-8 -*-
from decimal import Decimal

from db import CoinsDatabase


class CoinBase(object):
    def __init__(self):
        self.cdb = CoinsDatabase()

    def format_price(self, price):
        if price < 1:
            return Decimal('%.6f' % price)
        return Decimal('%.2f' % price)

    def format_diff(self, diff):
        if not diff:
            return ''

        abs_diff = 0 if int(abs(diff)) < 50 else 1

        if diff < 0:
            return '\x0305Down: {:,.2f}% Today\x03'.format(abs(diff))
        return '\x0303Up: {:,.2f}% Today\x03'.format(diff)


class Coins(CoinBase):
    def bulls(self):
        return self.get_movers()

    def bears(self):
        return self.get_movers('asc')

    def get_movers(self, order='desc'):
        prices = self.cdb.get_movers(order)
        formatted  = ['{Name} ({Nick}) {Diff} '.format(**self._format(p)) for p in prices] 
        return ''.join(formatted)

    def _format(self, p):
        fields = ['Name', 'Nick', 'First', 'Last', 'Diff']
        price = dict(zip(fields, p))
        price['Name'] = price['Name'].title()
        price['Nick'] = price['Nick'].upper()
        price['First'] = self.format_price(price['First'])
        price['Last'] = self.format_price(price['Last'])
        price['Diff'] = self.format_diff(price['Diff'])
        return price


class Coin(CoinBase):
    def __init__(self, c='btc'):
        super(Coin, self).__init__()
        all_coins = self.cdb.get_coins()
        self.coins = set(all_coins.keys())
        self.nicks = {v:k for k,v in all_coins.items()}
        self.name = self._name(c)

    def _name(self, c):
        coin = c.lower()
        if coin not in self.coins:
            coin = self.nicks.get(coin, 'bitcoin')
        return coin

    def price(self):
        return ('Current Price for {Name} ({Nick}): €{Euro:,} ${Dollar:,} 24h Low: €{Low:,} Median: €{Median:,} '
                '24h High: €{High:,} {Diff}').format(**self._price())

    def converter(self, amount):
        p = self._price()
        return '{} {} ({}) is worth €{:,} at €{:,} per coin'.format(amount, p['Name'], p['Nick'],
               self.format_price(p['Euro'] * amount), self.format_price(p['Euro']))

    def _price(self):
        fields = ['Name', 'Nick', 'Euro', 'Dollar', 'Low', 'High', 'Diff', 'Median']
        price = dict(zip(fields, self.cdb.get_latest_price(self.name)))
        price['Name'] = price['Name'].title()
        price['Nick'] = price['Nick'].upper()
        price['Median'] = self.format_price(price['Median'])
        price['Diff'] = self.format_diff(price['Diff'])
        return price


class Stats(Coin):
    def stats(self, date):
        return ('Stats for {Name} ({Nick}) on {Date}: Min €{Low:,} Mean €{Avg:,} Std Dev €{Std:,} '
                'Median €{Median:,} Max €{High:,}').format(**self._stats(date))

    def _stats(self, date):
        fields = ['Name', 'Nick', 'Date', 'Low', 'Avg', 'Median', 'Std', 'High']
        stats = dict(zip(fields, self.cdb.get_stats(self.name, date)))
        stats['Name'] = stats['Name'].title()
        stats['Nick'] = stats['Nick'].upper()
        stats['Median'] = self.format_price(stats['Median'])
        stats['Avg'] = self.format_price(stats['Avg'])
        stats['Std'] = self.format_price(stats['Std'])
        return stats


class ATS(Coin):
    def raw_ats(self):
        results = self.cdb.dated_ats(self.name)
        low_date, lowest = results[0]
        high_date, ath = results[1]
        return (low_date, self.format_price(lowest), high_date, self.format_price(ath))

    def ats(self):
        price = self._price()['Euro']
        lowest, ath = self.cdb.check_ats(self.name)
        if price >= ath:
            return 'New All Time High! BUY BUY BUY: %s' % self.price()

        if price <= lowest:
            return 'Dropping like a stone! SELL SELL SELL: %s' % self.price()


class Diff(Coin):
    def diff(self, date):
        return ('Diff for {Name} ({Nick}) from {Date} to {Latest}: First: €{First:,} Latest: €{Last:,} Diff: {Diff}'
               ).format(**self._diff(date))

    def _diff(self, date):
        fields = ['Name', 'Nick', 'Date', 'Latest', 'First', 'Last', 'Diff']
        diff = dict(zip(fields, self.cdb.get_diff(self.name, date)))
        diff['Name'] = diff['Name'].title()
        diff['Nick'] = diff['Nick'].upper()
        diff['First'] = self.format_price(diff['First'])
        diff['Last'] = self.format_price(diff['Last'])
        diff['Diff'] = self.format_diff(diff['Diff'])
        return diff


if __name__ == '__main__':
    pass
