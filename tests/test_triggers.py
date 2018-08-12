import unittest

from mooney import triggers


class TestMessage(object):

    class Source(object):
        def __init__(self, source='#channel', nick='test'):
            self.nick = nick
            self.user = nick
            self.source = source

    def __init__(self, msg):
        self.arguments = [msg]
        self.source = TestMessage.Source()


class TestTriggers(unittest.TestCase):
    def test_advice(self):
        self.assertEqual(triggers.Trigger.make(TestMessage('!advice')).message(), 'Don\'t buy bitcoin!')

    def test_coin(self):
        self.assertTrue(triggers.Trigger.make(TestMessage('!coin')).message().startswith(
                        'Current Price for Bitcoin (BTC):'))

    def test_fiat(self):
        self.assertTrue(triggers.Trigger.make(TestMessage('!fiat')).message().startswith(
                         '1 Bitcoin (BTC) is worth'))

    def test_help(self):
        self.assertEqual(triggers.Trigger.make(TestMessage('!help')).message(),
                         'Commands: !advice !ats !bears !bulls !help !coin !diff !fiat !stats. !help [command] for more information on a specific command.')

    def test_help_advice(self):
        self.assertTrue(triggers.Trigger.make(TestMessage('!help advice')).message().startswith('!advice'))

    def test_help_ats(self):
        self.assertTrue(triggers.Trigger.make(TestMessage('!help ats')).message().startswith('!ats'))

    def test_help_bears(self):
        self.assertTrue(triggers.Trigger.make(TestMessage('!help bears')).message().startswith('!bears'))

    def test_help_bulls(self):
        self.assertTrue(triggers.Trigger.make(TestMessage('!help bulls')).message().startswith('!bulls'))

    def test_help_coin(self):
        self.assertTrue(triggers.Trigger.make(TestMessage('!help coin')).message().startswith('!coin'))

    def test_help_diff(self):
        self.assertTrue(triggers.Trigger.make(TestMessage('!help diff')).message().startswith('!diff'))

    def test_help_fiat(self):
        self.assertTrue(triggers.Trigger.make(TestMessage('!help fiat')).message().startswith('!fiat'))

    def test_help_stats(self):
        self.assertTrue(triggers.Trigger.make(TestMessage('!help stats')).message().startswith('!stats'))


if __name__ == '__main__':
    unittest.main()
