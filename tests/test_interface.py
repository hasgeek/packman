# -*- coding: utf-8 -*-

from packman.models import db, Node, ConnectionInterface, GENDER
from .test_db import TestDatabaseFixture


class TestInterface(TestDatabaseFixture):
    def setUp(self):
        super(TestInterface, self).setUp()
        self.root = Node(name=u'interfaces', title=u"Interfaces")

    def make_usb_interfaces(self):
        self.usb2_type_a_male = ConnectionInterface(title=u"USB 2.0 Type A (male)", gender=GENDER.MALE, parent=self.root)
        self.usb2_type_a_female = ConnectionInterface(title=u"USB 2.0 Type A (female)", gender=GENDER.FEMALE, parent=self.root)
        self.usb2_type_b_male = ConnectionInterface(title=u"USB 2.0 Type B (male)", gender=GENDER.MALE, parent=self.root)
        self.usb2_type_b_female = ConnectionInterface(title=u"USB 2.0 Type B (female)", gender=GENDER.FEMALE, parent=self.root)

        self.usb3_type_a_male = ConnectionInterface(title=u"USB 3.0 Type A (male)", gender=GENDER.MALE, parent=self.root)
        self.usb3_type_a_female = ConnectionInterface(title=u"USB 3.0 Type A (female)", gender=GENDER.FEMALE, parent=self.root)
        self.usb3_type_b_male = ConnectionInterface(title=u"USB 3.0 Type B (male)", gender=GENDER.MALE, parent=self.root)
        self.usb3_type_b_female = ConnectionInterface(title=u"USB 3.0 Type B (female)", gender=GENDER.FEMALE, parent=self.root)

        db.session.add_all([self.usb2_type_a_male, self.usb2_type_a_female, self.usb2_type_b_male, self.usb2_type_b_female])
        db.session.add_all([self.usb3_type_a_male, self.usb3_type_a_female, self.usb3_type_b_male, self.usb3_type_b_female])
        db.session.commit()
        return 8  # Count of interfaces we created above

    def test_create_interfaces(self):
        count = self.make_usb_interfaces()
        self.assertEqual(ConnectionInterface.query.count(), count)
        self.assertEqual(len(self.root.nodes), count)

    def test_interface_coupling(self):
        self.make_usb_interfaces()

        self.usb2_type_a_female.couple_with(self.usb2_type_a_male)
        self.usb2_type_a_female.couple_with(self.usb3_type_a_male)

        self.usb3_type_a_female.couple_with(self.usb2_type_a_male)
        self.usb3_type_a_female.couple_with(self.usb3_type_a_male)

        self.usb2_type_b_female.couple_with(self.usb2_type_b_male)

        self.usb3_type_b_female.couple_with(self.usb2_type_b_male)
        self.usb3_type_b_female.couple_with(self.usb3_type_b_male)

        db.session.commit()

        self.assertEqual(set(self.usb2_type_a_female.couples), set([self.usb2_type_a_male, self.usb3_type_a_male]))
        self.assertEqual(set(self.usb3_type_a_female.couples), set([self.usb2_type_a_male, self.usb3_type_a_male]))
        self.assertEqual(set(self.usb2_type_b_female.couples), set([self.usb2_type_b_male]))
        self.assertEqual(set(self.usb3_type_b_female.couples), set([self.usb2_type_b_male, self.usb3_type_b_male]))

        self.assertEqual(set(self.usb2_type_a_male.couples), set([self.usb2_type_a_female, self.usb3_type_a_female]))
        self.assertEqual(set(self.usb3_type_a_male.couples), set([self.usb2_type_a_female, self.usb3_type_a_female]))
        self.assertEqual(set(self.usb2_type_b_male.couples), set([self.usb2_type_b_female, self.usb3_type_b_female]))
        self.assertEqual(set(self.usb3_type_b_male.couples), set([self.usb3_type_b_female]))
