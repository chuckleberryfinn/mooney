# -*- coding: utf-8 -*-
from db import CoinsDatabase


class Reply(object):
    def __init__(self):
        self.cdb = CoinsDatabase()


class Advice(Reply):
    def response(self):
        return self.cdb.get_advice()[0]


class Auto(Reply):
    def response(self, comment):
        c = self.cdb.get_remark(comment)
        return c[0] if c else None


class Targeted(Reply):
    def __init__(self, sender):
        super(Targeted, self).__init__()
        self.sender = sender

    def response(self, comment):
        c = self.cdb.get_targeted_remark(self.sender, comment)
        return c[0] if c else None


class Admin(Reply):
    def response(self, user):
        c = self.cdb.is_admin(user)
        return True if c else False


if __name__ == '__main__':
    pass
