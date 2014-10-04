# -*- coding: utf-8 -*-

import os
import unittest
from coaster.utils import buid
from packman import init_for, app, db, models

init_for('test')
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI', 'postgresql://postgres@localhost/myapp_test')


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
