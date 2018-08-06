# -*- coding: utf-8 -*-
import argparse
import logging
import threading
import time

import irc.bot

from triggers import Trigger, Auto, Alert


logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.INFO)


class Mooney(irc.bot.SingleServerIRCBot):
    def __init__(self, server, channel, nick):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, 6667)], nick, nick)
        self.nick = nick
        self.server = server
        self.channel = channel

    def on_nicknameinuse(self, c, _):
        c.nick('%s_' % c.get_nickname())

    def on_welcome(self, c, _):
        c.join(self.channel)
        self.send_alert()

    def send_alert(self):
        alert = Alert()
        msg = alert.message()
        self.send_privmsg(self.channel, msg)
        threading.Timer(60 * 5, self.send_alert).start()

    def on_privmsg(self, c, e):
        logging.info('%s said: %s to me', e.source.nick, e.arguments[0])
        self.on_message(e.source.nick, e)

    def on_pubmsg(self, c, e):
        logging.info('%s said: %s to: %s', e.source.nick, e.arguments[0], self.channel)
        self.on_message(self.channel, e)

    def on_message(self, recipient, e):
        command = Trigger.make(e)
        if isinstance(command, Auto) and e.type == 'privmsg':
            return

        self.send_privmsg(recipient, command.message())

    def send_privmsg(self, recipient, msg):
        if not msg:
            return

        try:
            self.connection.privmsg(recipient, msg)
        except:
            logging.exception("Exception sending message")
            return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mooney IRC Bot.')
    parser.add_argument('server', type=str, help='Server to connect to.')
    parser.add_argument('channel', type=str, help='Channel to join.')
    parser.add_argument('--nickname', type=str, default='mooney', help='Bot name (default mooney).')

    args = parser.parse_args()
    channel = '%s' % args.channel if args.channel.startswith('#') else '#%s' % args.channel

    while True:
        try:
            mooney = Mooney(args.server, channel, args.nickname)
            mooney.start()
        except:
            logging.exception("")
            mooney.die()
        time.sleep(120)
