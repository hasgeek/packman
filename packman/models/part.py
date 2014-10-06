# -*- coding: utf-8 -*-

from . import db, TimestampMixin, NodeMixin, Node
from .interface import ConnectionInterface

__all__ = ['PartInterface', 'Part', 'PartInstance']


class PartInterface(TimestampMixin, db.Model):
    __tablename__ = 'part_interface'
    part_id = db.Column(None, db.ForeignKey('part.id'), primary_key=True)
    # PartInterface.part is defined in the backref from Part
    interface_id = db.Column(None, db.ForeignKey('interface.id'), primary_key=True)
    interface = db.relationship(ConnectionInterface, backref=db.backref('interface_parts', cascade='all, delete-orphan'))
    count = db.Column(db.Integer, nullable=False, default=1)


class Part(NodeMixin, Node):
    __tablename__ = 'part'
    #: Description of the item
    description = db.Column(db.UnicodeText)
    part_interfaces = db.relationship(PartInterface, cascade='all, delete-orphan', backref='part')
    #: TODO: Other metadata such as price

    def compatible_with(self, part):
        """
        Do we have an interface that is coupled with one of the interfaces on the other part?
        """
        if isinstance(part, Part):
            # TODO: Delegate this to the database with an SQL join query
            local_interfaces = [pi.interface for pi in self.part_interfaces]
            remote_interfaces = [pi.interface for pi in part.part_interfaces]

            for li in local_interfaces:
                for ri in remote_interfaces:
                    if li in ri.couples:
                        return True
        return False


class PartInstance(NodeMixin, Node):
    __tablename__ = 'part_instance'
    part_id = db.Column(None, db.ForeignKey('part.id'))
    part = db.relationship(Part, foreign_keys=[part_id], backref=db.backref('instances', cascade='all, delete-orphan'))
    #: Description of this particular instance (health notes, acquisition story, etc)
    description = db.Column(db.UnicodeText)
    # TODO: Include columns here to describe acquisition date, owner, possessor, etc
