# -*- coding: utf-8 -*-

from packman.models import db, Node, Category
from .test_db import TestDatabaseFixture
from .test_interface import InterfaceHelper


class CategoryHelper(object):
    def __init__(self):
        self.ih = InterfaceHelper()
        self.root = Node(name=u'categories', title=u"Categories", itype=u'categories')
        db.session.add(self.root)
        self.ih.make_usb_interfaces()
        self.ih.make_usb_couples()

    def make_categories(self):
        cables = Category(name=u'cables', title=u"Cables and adapters", parent=self.root)
        Category(name=u'power', title=u"Power adapters", parent=cables)

        usb = Category(name=u'usb', title=u"USB cables", parent=cables)
        usb1 = Category(name=u'typeb2', title=u"USB 2.0 Type B (square) cables", parent=usb)
        usb1.interfaces.append(self.ih.root.nodes['usb2-type-a-male'])
        usb1.interfaces.append(self.ih.root.nodes['usb2-type-b-male'])

        usb2 = Category(name=u'typeb3', title=u"USB 3.0 Type B (square) cables", parent=usb)
        usb2.interfaces.append(self.ih.root.nodes['usb3-type-a-male'])
        usb2.interfaces.append(self.ih.root.nodes['usb3-type-b-male'])

        db.session.commit()
        return 5  # Number of categories created above


class TestCategory(TestDatabaseFixture):
    def setUp(self):
        super(TestCategory, self).setUp()
        self.helper = CategoryHelper()

    def test_categorytree(self):
        count = self.helper.make_categories()
        self.assertEqual(Category.query.count(), count)

    def test_categories_have_interfaces(self):
        self.helper.make_categories()
        cables = self.helper.root.nodes['cables']
        usb = cables.nodes['usb']
        typeb2 = usb.nodes['typeb2']
        self.assertEqual(
            set(typeb2.interfaces),
            set([self.helper.ih.root.nodes['usb2-type-a-male'], self.helper.ih.root.nodes['usb2-type-b-male']]))

    # TODO: Test adding parts to categories: they should acquire interfaces automatically
