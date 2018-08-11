# -*- coding: utf-8 -*-
import datetime
import decimal
import logging

from datetime import date, datetime, timedelta
from decimal import Decimal

import responses


logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.INFO)


class Trigger(object):
    triggers = set()
    last_msg = None
    delay = None
    help_message = ('Commands: !advice !ats !bears !bulls !help !coin !diff !fiat !stats. ' +
                    '!help [command] for more information on a specific command.')

    @classmethod
    def make(cls, e):
        msgs = e.arguments[0].split()
        for c in cls.__subclasses__():
            if msgs[0].lower() in c.triggers:
                return c(e)
        return Auto.make(e)

    def __init__(self, e):
        self.msgs = e.arguments[0].split()
        self.sender_nick = e.source.nick.lower() if e.source else None
        self.sender = e.source.user.lower() if e.source else None

    def parse_coin_date(self):
        if len(self.msgs) == 1:
            coin = 'btc'
            d = date.today() - timedelta(days=1)
        elif len(self.msgs) == 2:
            try:
                d = datetime.strptime(self.msgs[1], '%Y-%m-%d').date()
            except ValueError:
                coin = self.msgs[1]
                d = date.today() - timedelta(days=1)
            else:
                coin = 'btc'
        else:
            coin = self.msgs[1]
            try:
                d = datetime.strptime(self.msgs[2], '%Y-%m-%d').date()
            except ValueError:
                d = date.today() - timedelta(days=1)

        if d <= datetime.strptime('2017-12-12', '%Y-%m-%d').date() or d >= date.today():
            d = date.today() - timedelta(days=1)

        return coin, d

    @classmethod
    def cool_down(cls): 
        if not cls.delay:
            return False

        if cls.last_msg and cls.last_msg > (datetime.utcnow() - cls.delay):
            return True

        cls.last_msg = datetime.utcnow()
        return False

    def message(self):
        if not self.cool_down():
            command = ''
            try:
                command = self.command.get_response()
            except:
                logging.exception('')
            return command


class Price(Trigger):
    triggers = set(['!coin', '!crack', '!price'])
    help_message = '!coin [coin|ticker]: Get current price for a coin. Defaults to btc.'

    def __init__(self, e):
        super(Price, self).__init__(e)
        coin = self.msgs[1] if len(self.msgs) >= 2 else 'bitcoin'
        self.coin = coin
        self.command = responses.Price(self.coin)


class Advice(Trigger):
    triggers = set(['!advice'])
    delay = timedelta(seconds=20)
    help_message = '!advice: Some of mooney''s sage advice'

    def __init__(self, e):
        super(Advice, self).__init__(e)
        self.command = responses.Advice()


class Ats(Trigger):
    triggers = set(['!ats', '!ath'])
    delay = timedelta(seconds=20)
    help_message = '!ats [coin]: All time highs and lows (since 2017-12-12) for a coin. Defaults to bitcoin.'

    def __init__(self, e):
        super(Ats, self).__init__(e)
        coin = self.msgs[1] if len(self.msgs) >= 2 else 'bitcoin'
        self.coin = coin
        self.command = responses.Ats(self.coin)


class Control(Trigger):
    triggers = set(['!shush', '!alerts'])
    enabled = True

    def message(self):
        if not responses.Admin(self.sender).get_response():
            return

        if self.msgs[0].lower() == '!shush':
            if not Control.enabled:
                return

            Control.enabled = False
            return 'Shutting up!'

        if Control.enabled:
            return

        Control.enabled = True
        return 'Alerts enabled!'

    @classmethod
    def can_send(cls):
        return cls.enabled


class Alert(Trigger):
    delay = timedelta(hours=1)
    def __init__(self):
        pass

    def message(self):
        alert_msg = responses.Alert().get_response('btc')
        if not alert_msg:
            return

        if self.cool_down():
            return

        if not Control.can_send():
            return

        logging.info('Alerting on price')
        return alert_msg


class Auto(Trigger):
    delay = timedelta(minutes=2)

    @classmethod
    def make(cls, e):
        try:
            return Targeted(e)
        except ValueError:
            return Auto(e)

    def message(self):
        resp = responses.Auto().get_response(' '.join(self.msgs))

        if not resp or self.cool_down():
            return

        return resp


class Targeted(Auto):
    def __init__(self, e):
        super(Targeted, self).__init__(e)
        self.response = responses.Targeted(self.sender).get_response(' '.join(self.msgs))

        if not self.response:
            raise ValueError

    def message(self):
        if self.cool_down():
            return

        return self.response


class Stats(Trigger):
    triggers = set(['!stats'])
    help_message = ('!stats [coin|ticker] [date]: Get the statistics for a coin''s price over the course of a day. ' +
                    'Defaults to btc and yesterday''s date.')

    def __init__(self, e):
        super(Stats, self).__init__(e)

        coin, target_date = self.parse_coin_date()
        self.command = responses.Stats(coin, target_date)


class Bulls(Trigger):
    triggers = set(['!bulls'])
    help_message = '!bulls: Get today''s big winners.'

    def __init__(self, e):
        super(Bulls, self).__init__(e)
        self.command = responses.Bulls()


class Bears(Trigger):
    triggers = set(['!bears'])
    help_message = '!bears: Get today''s big losers.'

    def __init__(self, e):
        super(Bears, self).__init__(e)
        self.command = responses.Bears()


class Fiat(Trigger):
    triggers = set(['!fiat'])
    help_message = ('!fiat [coin|ticker] [amount]: Get the current price in fiat for an amount of coins. ' +
                    'Defaults to btc and 1 coin.')

    def __init__(self, e):
        super(Fiat, self).__init__(e)
        amount = 1
        coin = 'btc'

        if len(self.msgs) == 2:
            try:
                amount = Decimal(self.msgs[1])
            except decimal.InvalidOperation:
                coin = self.msgs[1]
        elif len(self.msgs) > 2:
            coin = self.msgs[1]
            try:
                amount = Decimal(self.msgs[2])
            except decimal.InvalidOperation:
                pass

        self.command = responses.Fiat(coin, amount)


class Diff(Trigger):
    triggers = set(['!diff'])
    help_message = ('!diff [coin|ticker] [date]: Get the difference in price between the start date and current price.'
                    + ' Defaults to btc and yesterday''s date.')

    def __init__(self, e):
        super(Diff, self).__init__(e)

        coin, target_date = self.parse_coin_date()
        self.command = responses.Diff(coin, target_date)


class Help(Trigger):
    triggers = set(['!help', '!halp'])

    def __init__(self, e):
        super(Help, self).__init__(e)
        self.response = self.help_message

        if len(self.msgs) == 1:
            return

        for cls in Trigger.__subclasses__():
            if '!%s' % self.msgs[1].lower() in cls.triggers:
                self.response = cls.help_message
                break

    def message(self):
        return self.response


if __name__ == '__main__':
    pass
