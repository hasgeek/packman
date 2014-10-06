# -*- coding: utf-8 -*-

from packman.models import db, Node, Part
from .test_db import TestDatabaseFixture
from .test_interface import InterfaceHelper

class PartHelper:
    def __init__(self):
        self.ih = InterfaceHelper()
        self.ih.make_usb_interfaces()
        self.ih.make_usb_couples()
        self.root = Node(name=u'parts',title=u'Parts',itype=u'parts')
        db.session.add(self.root)

    def make_parts(self):
         # add 4 parts usb2 cable, usb3 cable, computer, phone with interfaces
        usb2 = Part(name=u'usb2', title=u"USB 2.0 cable", parent=self.root)
        usb2.interfaces.append(self.ih.root.nodes['usb2-type-a-male'])
        usb2.interfaces.append(self.ih.root.nodes['usb2-type-b-male'])

        usb3 = Part(name=u'usb3', title=u"USB 3.0 cable", parent=self.root)
        usb3.interfaces.append(self.ih.root.nodes['usb3-type-a-male'])
        usb3.interfaces.append(self.ih.root.nodes['usb3-type-b-male'])

        printer = Part(name=u'printer', title=u"Printer", parent=self.root)
        printer.interfaces.append(self.ih.root.nodes['usb2-type-b-female'])

        laptop = Part(name=u'laptop', title=u"Laptop", parent=self.root)
        laptop.interfaces.append(self.ih.root.nodes['usb3-type-a-female'])

        return 4 # Number of parts created


class TestPart(TestDatabaseFixture):
    def setUp(self):
        super(TestPart, self).setUp()
        self.helper = PartHelper()

    def test_part_exists(self):
        count = self.helper.make_parts()
        self.assertEqual(Part.query.count(), count)

    def test_parts_have_interfaces(self):
        self.helper.make_parts()
        self.assertEqual(
            set(self.helper.root.nodes['usb2'].interfaces),
            set([self.helper.ih.root.nodes['usb2-type-a-male'], self.helper.ih.root.nodes['usb2-type-b-male']]))
        self.assertEqual(
            set(self.helper.root.nodes['usb3'].interfaces),
            set([self.helper.ih.root.nodes['usb3-type-a-male'], self.helper.ih.root.nodes['usb3-type-b-male']]))
        self.assertEqual(
            set(self.helper.root.nodes['printer'].interfaces),
            set([self.helper.ih.root.nodes['usb2-type-b-female']]))
        self.assertFalse(self.helper.ih.root.nodes['usb2-type-a-female'] in self.helper.root.nodes['laptop'].interfaces)
        self.assertTrue(self.helper.ih.root.nodes['usb3-type-a-female'] in self.helper.root.nodes['laptop'].interfaces)

    def test_part_compatibility(self):
        self.helper.make_parts()
        nodes = self.helper.root.nodes
        self.assertTrue(nodes['usb2'].is_compatible_with(nodes['printer']))
        self.assertTrue(nodes['usb2'].is_compatible_with(nodes['laptop']))
        self.assertFalse(nodes['usb3'].is_compatible_with(nodes['printer']))
        self.assertTrue(nodes['usb3'].is_compatible_with(nodes['laptop']))
