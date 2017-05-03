# -*- coding: utf-8 -*-

from packman.models import db, Node, Bundle, PartInstance
from .test_db import TestDatabaseFixture
from .test_interface import InterfaceHelper
from .test_part import PartHelper


class BundleHelper(object):
    def __init__(self):
        self.ih = InterfaceHelper()
        self.ph = PartHelper()
        self.ph.make_parts()
        self.root = Node(name=u'bundles', title=u'Bundles', itype=u'bundles')
        db.session.add(self.root)

    def make_bundle(self):
        # Create two bundles - programmer_kit and computer box
        programmer_kit = Bundle(name=u'programmer-kit', title=u"HasGeek Programmer Kit L-1", parent=self.root)
        Bundle(name=u'computer-box', title=u"Macbook Pro Carton", parent=programmer_kit)

    def make_part_instance(self):
        # Add part instances to bundles
        computer_box = self.root.nodes['programmer-kit'].nodes['computer-box']
        laptop = PartInstance(part=self.ph.root.nodes['laptop'], parent=computer_box)
        PartInstance(part=self.ph.root.nodes['power-adapter'], parent=computer_box)
        PartInstance(part=self.ph.root.nodes['ram-4gb'], parent=laptop)
        PartInstance(part=self.ph.root.nodes['ram-4gb'], parent=laptop)
        PartInstance(part=self.ph.root.nodes['keyboard'], parent=self.root.nodes['programmer-kit'])
        PartInstance(part=self.ph.root.nodes['mouse'], parent=self.root.nodes['programmer-kit'])


class TestBundle(TestDatabaseFixture):
    def setUp(self):
        super(TestBundle, self).setUp()
        self.helper = BundleHelper()

    def test_bundle_matches_spec(self):
        self.helper.make_bundle()
        self.helper.make_part_instance()
        nodes = self.helper.root.nodes
        programmer_kit_l1 = {
            'laptop': 1,
            'ram-4gb': 2,
            'power-adapter': 1,
            'keyboard': 1,
            'mouse': 1,
            }
        self.assertEqual(programmer_kit_l1, dict([(sp.part.name, sp.count) for sp in nodes['programmer-kit'].make_spec().specparts]))

        # Increase count of a part(RAM) and rerun test
        programmer_kit_l2 = {
            'laptop': 1,
            'ram-4gb': 3,
            'power-adapter': 1,
            'keyboard': 1,
            'mouse': 1,
            }
        PartInstance(part=self.helper.ph.root.nodes['ram-4gb'], parent=nodes['programmer-kit'])
        self.assertEqual(programmer_kit_l2, dict([(sp.part.name, sp.count) for sp in nodes['programmer-kit'].make_spec().specparts]))

        # Add a part(USB 3.0) and rerun test
        programmer_kit_l3 = {
            'laptop': 1,
            'ram-4gb': 3,
            'power-adapter': 1,
            'keyboard': 1,
            'mouse': 1,
            'usb3': 1,
            }
        PartInstance(name=u'hispeedusb', part=self.helper.ph.root.nodes['usb3'], parent=nodes['programmer-kit'])
        self.assertEqual(programmer_kit_l3, dict([(sp.part.name, sp.count) for sp in nodes['programmer-kit'].make_spec().specparts]))

        # Remove a part(USB 3.0) and rerun test
        programmer_kit_l4 = {
            'laptop': 1,
            'ram-4gb': 3,
            'power-adapter': 1,
            'keyboard': 1,
            'mouse': 1,
            }
        nodes['programmer-kit'].nodes.pop(u'hispeedusb')
        self.assertEqual(programmer_kit_l4, dict([(sp.part.name, sp.count) for sp in nodes['programmer-kit'].make_spec().specparts]))
