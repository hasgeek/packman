# -*- coding: utf-8 -*-

from packman.models import db, Node, Part, PartInterface
from .test_db import TestDatabaseFixture
from .test_interface import InterfaceHelper

class PartHelper:
    def __init__(self):
        self.ih = InterfaceHelper()
        self.ih.make_usb_interfaces()
        self.root = Node(name=u'parts',title=u'Parts',itype=u'parts')
        db.session.add(self.root)

    def make_part(self):

         # add 4 parts usb2 cable, usb3 cable, computer, phone with interfaces

        cable2 = Part(name=u'usb2', title=u"USB 2.0 cable", parent=self.root)
        cable2.part_interfaces.append(
            PartInterface(interface=self.ih.root.nodes['usb2-type-a-male']))
        cable2.part_interfaces.append(
            PartInterface(interface=self.ih.root.nodes['usb2-type-b-male']))

        cable3 = Part(name=u'usb3', title=u"USB 3.0 cable", parent=self.root)
        cable3.part_interfaces.append(
            PartInterface(interface=self.ih.root.nodes['usb3-type-a-male']))
        cable3.part_interfaces.append(
            PartInterface(interface=self.ih.root.nodes['usb3-type-b-male']))
          
        
        smartphone = Part(name=u'smartphone', title=u"Smartphone", parent=self.root)
        smartphone.part_interfaces.append(
            PartInterface(interface=self.ih.root.nodes['usb2-type-a-female']))
      
        laptop = Part(name=u'laptop', title=u"Laptop", parent=self.root)
        laptop.part_interfaces.append(
            PartInterface(interface=self.ih.root.nodes['usb3-type-a-female']))

        return 4 # Number of parts created
        


class TestPart(TestDatabaseFixture):
    def setUp(self):
        super(TestPart, self).setUp()
        self.helper = PartHelper()

    def test_part_exists(self):
        count = self.helper.make_part()
        self.assertEqual(Part.query.count(), count)

    def test_parts_have_interfaces(self):
        self.helper.make_part()
        self.assertEqual(
            set([pi.interface for pi in self.helper.root.nodes['usb2'].part_interfaces]),
            set([self.helper.ih.root.nodes['usb2-type-a-male'], self.helper.ih.root.nodes['usb2-type-b-male']]))
        self.assertEqual(
            set([pi.interface for pi in self.helper.root.nodes['usb3'].part_interfaces]),
            set([self.helper.ih.root.nodes['usb3-type-a-male'], self.helper.ih.root.nodes['usb3-type-b-male']]))
        self.assertEqual(
            set([pi.interface for pi in self.helper.root.nodes['smartphone'].part_interfaces]),
            set([self.helper.ih.root.nodes['usb2-type-a-female']]))
        self.assertFalse(self.helper.ih.root.nodes['usb2-type-a-female'] in self.helper.root.nodes['laptop'].interfaces)
        self.assertTrue(self.helper.ih.root.nodes['usb3-type-a-female'] in self.helper.root.nodes['laptop'].interfaces)

    def test_part_compatibility(self):
        self.helper.make_part()
        nodes = self.helper.root.nodes
        self.assertTrue(nodes['usb2'].is_compatible_with(nodes['smartphone']))
        self.assertTrue(nodes['usb2'].is_compatible_with(nodes['laptop']))
        self.assertFalse(nodes['usb3'].is_compatible_with(nodes['smartphone']))
        self.assertTrue(nodes['usb3'].is_compatible_with(nodes['laptop']))
