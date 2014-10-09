# -*- coding: utf-8 -*-

from packman.models import db, Node, ConnectionInterface, GENDER
from .test_db import TestDatabaseFixture


class InterfaceHelper(object):
    def __init__(self):
        self.root = Node(name=u'interfaces', title=u"Interfaces", itype=u'interfaces')
        db.session.add(self.root)

    def make_usb_interfaces(self):
        ConnectionInterface(name=u'usb2-type-a-male',   title=u"USB 2.0 Type A (male)",   gender=GENDER.MALE,   parent=self.root)
        ConnectionInterface(name=u'usb2-type-a-female', title=u"USB 2.0 Type A (female)", gender=GENDER.FEMALE, parent=self.root)
        ConnectionInterface(name=u'usb2-type-b-male',   title=u"USB 2.0 Type B (male)",   gender=GENDER.MALE,   parent=self.root)
        ConnectionInterface(name=u'usb2-type-b-female', title=u"USB 2.0 Type B (female)", gender=GENDER.FEMALE, parent=self.root)

        ConnectionInterface(name=u'usb3-type-a-male',   title=u"USB 3.0 Type A (male)",   gender=GENDER.MALE,   parent=self.root)
        ConnectionInterface(name=u'usb3-type-a-female', title=u"USB 3.0 Type A (female)", gender=GENDER.FEMALE, parent=self.root)
        ConnectionInterface(name=u'usb3-type-b-male',   title=u"USB 3.0 Type B (male)",   gender=GENDER.MALE,   parent=self.root)
        ConnectionInterface(name=u'usb3-type-b-female', title=u"USB 3.0 Type B (female)", gender=GENDER.FEMALE, parent=self.root)

        db.session.commit()
        return 8  # Count of interfaces we created above

    def make_usb_couples(self):
        nodes = self.root.nodes

        nodes['usb2-type-a-female'].couple_with(nodes['usb2-type-a-male'])
        nodes['usb2-type-a-female'].couple_with(nodes['usb3-type-a-male'])

        nodes['usb3-type-a-female'].couple_with(nodes['usb2-type-a-male'])
        nodes['usb3-type-a-female'].couple_with(nodes['usb3-type-a-male'])

        nodes['usb2-type-b-female'].couple_with(nodes['usb2-type-b-male'])

        nodes['usb3-type-b-female'].couple_with(nodes['usb2-type-b-male'])
        nodes['usb3-type-b-female'].couple_with(nodes['usb3-type-b-male'])

        db.session.commit()
        return 7  # Count of couples we created above

    def make_usb_couples_reverse(self):
        nodes = self.root.nodes

        nodes['usb2-type-a-male'].couple_with(nodes['usb2-type-a-female'])
        nodes['usb3-type-a-male'].couple_with(nodes['usb2-type-a-female'])

        nodes['usb2-type-a-male'].couple_with(nodes['usb3-type-a-female'])
        nodes['usb3-type-a-male'].couple_with(nodes['usb3-type-a-female'])

        nodes['usb2-type-b-male'].couple_with(nodes['usb2-type-b-female'])

        nodes['usb2-type-b-male'].couple_with(nodes['usb3-type-b-female'])
        nodes['usb3-type-b-male'].couple_with(nodes['usb3-type-b-female'])

        db.session.commit()
        return 7  # Count of couples we created above


class TestInterface(TestDatabaseFixture):
    def setUp(self):
        super(TestInterface, self).setUp()
        self.helper = InterfaceHelper()

    def test_create_interfaces(self):
        count = self.helper.make_usb_interfaces()
        self.assertEqual(ConnectionInterface.query.count(), count)
        self.assertEqual(len(self.helper.root.nodes), count)

    def test_interface_coupling(self):
        self.helper.make_usb_interfaces()
        self.helper.make_usb_couples()
        nodes = self.helper.root.nodes

        self.assertEqual(set(nodes['usb2-type-a-female'].couples), set([nodes['usb2-type-a-male'], nodes['usb3-type-a-male']]))
        self.assertEqual(set(nodes['usb3-type-a-female'].couples), set([nodes['usb2-type-a-male'], nodes['usb3-type-a-male']]))
        self.assertEqual(set(nodes['usb2-type-b-female'].couples), set([nodes['usb2-type-b-male']]))
        self.assertEqual(set(nodes['usb3-type-b-female'].couples), set([nodes['usb2-type-b-male'], nodes['usb3-type-b-male']]))

        self.assertEqual(set(nodes['usb2-type-a-male'].couples), set([nodes['usb2-type-a-female'], nodes['usb3-type-a-female']]))
        self.assertEqual(set(nodes['usb3-type-a-male'].couples), set([nodes['usb2-type-a-female'], nodes['usb3-type-a-female']]))
        self.assertEqual(set(nodes['usb2-type-b-male'].couples), set([nodes['usb2-type-b-female'], nodes['usb3-type-b-female']]))
        self.assertEqual(set(nodes['usb3-type-b-male'].couples), set([nodes['usb3-type-b-female']]))

    def test_interface_recoupling(self):
        self.helper.make_usb_interfaces()
        self.helper.make_usb_couples()
        self.helper.make_usb_couples_reverse()  # This should make no difference
        nodes = self.helper.root.nodes

        self.assertEqual(set(nodes['usb2-type-a-female'].couples), set([nodes['usb2-type-a-male'], nodes['usb3-type-a-male']]))
        self.assertEqual(set(nodes['usb3-type-a-female'].couples), set([nodes['usb2-type-a-male'], nodes['usb3-type-a-male']]))
        self.assertEqual(set(nodes['usb2-type-b-female'].couples), set([nodes['usb2-type-b-male']]))
        self.assertEqual(set(nodes['usb3-type-b-female'].couples), set([nodes['usb2-type-b-male'], nodes['usb3-type-b-male']]))

        self.assertEqual(set(nodes['usb2-type-a-male'].couples), set([nodes['usb2-type-a-female'], nodes['usb3-type-a-female']]))
        self.assertEqual(set(nodes['usb3-type-a-male'].couples), set([nodes['usb2-type-a-female'], nodes['usb3-type-a-female']]))
        self.assertEqual(set(nodes['usb2-type-b-male'].couples), set([nodes['usb2-type-b-female'], nodes['usb3-type-b-female']]))
        self.assertEqual(set(nodes['usb3-type-b-male'].couples), set([nodes['usb3-type-b-female']]))

    def test_interface_decoupling1(self):
        self.helper.make_usb_interfaces()
        self.helper.make_usb_couples()
        nodes = self.helper.root.nodes

        self.assertEqual(set(nodes['usb3-type-b-female'].couples), set([nodes['usb2-type-b-male'], nodes['usb3-type-b-male']]))
        nodes['usb3-type-b-female'].decouple_with(nodes['usb2-type-b-male'])
        self.assertEqual(set(nodes['usb3-type-b-female'].couples), set([nodes['usb3-type-b-male']]))

    def test_interface_decoupling2(self):
        self.helper.make_usb_interfaces()
        self.helper.make_usb_couples()
        nodes = self.helper.root.nodes

        self.assertEqual(set(nodes['usb3-type-b-female'].couples), set([nodes['usb2-type-b-male'], nodes['usb3-type-b-male']]))
        nodes['usb2-type-b-male'].decouple_with(nodes['usb3-type-b-female'])
        self.assertEqual(set(nodes['usb3-type-b-female'].couples), set([nodes['usb3-type-b-male']]))
