# -*- coding: utf-8 -*-

import unittest
from coaster.utils import buid
from packman import init_for, app, db, models

init_for('testing')


class TestDatabaseFixture(unittest.TestCase):
    def setUp(self):
        self.app = app
        db.create_all()
        self.user1 = models.User(username=u'user1', userid=buid())
        db.session.add(self.user1)
        app.testing = True

    def tearDown(self):
        db.session.rollback()
        db.drop_all()
        db.session.remove()
