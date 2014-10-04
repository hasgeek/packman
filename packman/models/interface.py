# -*- coding: utf-8 -*-

from coaster.utils import LabeledEnum
from baseframe import __
from . import db, NodeMixin, Node, make_timestamp_columns

__all__ = ['GENDER', 'ConnectionInterface']


class GENDER(LabeledEnum):
    UNKNOWN = (0, 'unknown', __("Unknown"))
    NA = (1, 'na', __("NA (genderless)"))
    MALE = (2, 'male', __("Male (plug)"))
    FEMALE = (3, 'female', __("Female (jack/socket)"))


#: Link related interfaces together. SQL does not support commutative relationships,
#: so LHS+RHS is not the same as RHS+LHS. We work around this by providing a virtual
#: :attr:`ConnectionInterface.couples` property that combines relationships in both
#: directions, plus the :meth:`ConnectionInterface.couple_with` method to couple
#: with an interface only if it's not already coupled with in either direction.
interface_coupling_table = db.Table('interface_coupling', db.Model.metadata,
    *(make_timestamp_columns() + (
        db.Column('lhs_interface_id', None, db.ForeignKey('interface.id'), primary_key=True),
        db.Column('rhs_interface_id', None, db.ForeignKey('interface.id'), primary_key=True)
        )))


class ConnectionInterface(NodeMixin, Node):
    __tablename__ = 'interface'
    description = db.Column(db.UnicodeText)
    #: Is this interface male, female or genderless?
    gender = db.Column(db.SmallInteger, default=GENDER.UNKNOWN, nullable=False)
    _couples_rhs = db.relationship('ConnectionInterface', secondary=interface_coupling_table,
        primaryjoin='ConnectionInterface.id == interface_coupling.c.lhs_interface_id',
        secondaryjoin='ConnectionInterface.id == interface_coupling.c.rhs_interface_id',
        backref='_couples_lhs')

    #: Other interfaces that this interface is directly compatible with. This is
    #: usually a male+female relationship of one type of interface, but sometimes
    #: can be across types. For example, USB 3.0 Type B female can accept both
    #: USB 3.0 Type B male and USB 2.0 Type B male. However, the USB 3.0 Type B
    #: male interface is NOT compatible with the USB 2.0 Type B female.
    @property
    def couples(self):
        return frozenset(self._couples_lhs + self._couples_rhs)

    def couple_with(self, interface):
        """
        Couple this interface with another interface.
        """
        if isinstance(interface, ConnectionInterface) and interface not in self.couples:
            self._couples_lhs.append(interface)

    def decouple_with(self, interface):
        """
        Decouple this interface with another interface.
        """
        if isinstance(interface, ConnectionInterface):
            if interface in self._couples_lhs:
                self._couples_lhs.remove(interface)
            if interface in self._couples_rhs:
                self._couples_rhs.remove(interface)

    def as_dict(self):
        """Export this interface as a dictionary."""
        retval = super(ConnectionInterface, self).as_dict()
        retval['gender'] = GENDER[self.gender].name
        retval['couples'] = [{'buid': i.buid, 'name': i.name} for i in self.couples]
        return retval

    def import_from(self, data):
        """Import from a dictionary."""
        retval = super(ConnectionInterface, self).import_from(data)
        self.gender = GENDER.value_for(data.get('gender', GENDER.UNKNOWN))
        return retval

    def import_from_internal(self, data):
        """Import internal references."""
        retval = super(ConnectionInterface, self).import_from_internal(data)
        for i in data.get('couples', []):
            interface = ConnectionInterface.get(i['buid'])
            if interface is None:
                interface = ConnectionInterface.get(i['name'])
            if interface is not None:
                self.couple_with(interface)
        return retval
