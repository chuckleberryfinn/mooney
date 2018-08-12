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
        self.assertEqual(triggers.Trigger.make(TestMessage('!fiat')).message(),
                         '1 Bitcoin (BTC) is worth €5,452.41 at €5,452.41 per coin')

    def test_help(self):
        self.assertEqual(triggers.Trigger.make(TestMessage('!help')).message(),
                         'Commands: !advice !ats !bears !bulls !help !coin !diff !fiat !stats. !help [command] for more information on a specific command.')


if __name__ == '__main__':
    unittest.main()
