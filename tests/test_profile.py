# -*- coding: utf-8 -*-

from packman.models import db, Node
from .test_db import TestDatabaseFixture


class ProfileHelper(object):
    def __init__(self):
        self.root = Node(name=u'profiles', title=u'Profiles', itype=u'profiles')
        db.session.add(self.root)


class TestProfile(TestDatabaseFixture):
    def setUp(self):
        pass
