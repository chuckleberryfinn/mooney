import unittest

from irc.client import Event, NickMask

from mooney import triggers


class TestTriggers(unittest.TestCase):
    def test_advice(self):
        self.assertEqual(triggers.Trigger.make(self.create_event('!advice')).message(), 'Don\'t date robots!')

    def test_coin(self):
        self.assertTrue(triggers.Trigger.make(self.create_event('!coin')).message().startswith(
                        'Current Price for Bitcoin (BTC):'))

    def test_fiat(self):
        self.assertTrue(triggers.Trigger.make(self.create_event('!fiat')).message().startswith(
                         '1 Bitcoin (BTC) is worth'))

    def test_stats(self):
        self.assertTrue(triggers.Trigger.make(self.create_event('!stats')).message().startswith(
                         'Stats for Bitcoin'))

    def test_help(self):
        self.assertEqual(triggers.Trigger.make(self.create_event('!help')).message(),
                        ('Commands: !advice !ats !bears !bulls !help !coin !diff !fiat !stats. ' +
                         '!help [command] for more information on a specific command.'))

    def test_help_advice(self):
        self.assertTrue(triggers.Trigger.make(self.create_event('!help advice')).message().startswith('!advice'))

    def test_help_ats(self):
        self.assertTrue(triggers.Trigger.make(self.create_event('!help ats')).message().startswith('!ats'))

    def test_help_bears(self):
        self.assertTrue(triggers.Trigger.make(self.create_event('!help bears')).message().startswith('!bears'))

    def test_help_bulls(self):
        self.assertTrue(triggers.Trigger.make(self.create_event('!help bulls')).message().startswith('!bulls'))

    def test_help_coin(self):
        self.assertTrue(triggers.Trigger.make(self.create_event('!help coin')).message().startswith('!coin'))

    def test_help_diff(self):
        self.assertTrue(triggers.Trigger.make(self.create_event('!help diff')).message().startswith('!diff'))

    def test_help_fiat(self):
        self.assertTrue(triggers.Trigger.make(self.create_event('!help fiat')).message().startswith('!fiat'))

    def test_help_stats(self):
        self.assertTrue(triggers.Trigger.make(self.create_event('!help stats')).message().startswith('!stats'))

    def create_event(self, msg):
        return Event('privmsg', NickMask('user!username@example.com'), '#channel', [msg])


if __name__ == '__main__':
    unittest.main()
