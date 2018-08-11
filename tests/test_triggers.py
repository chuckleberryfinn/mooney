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
    def test_coin(self):
        self.assertTrue(triggers.Trigger.make(TestMessage('!coin')).message().startswith(
                        'Current Price for Bitcoin (BTC):'))

    def test_advice(self):
        self.assertEqual(triggers.Trigger.make(TestMessage('!advice')).message(), 'Don\'t buy bitcoin!')


if __name__ == '__main__':
    unittest.main()
