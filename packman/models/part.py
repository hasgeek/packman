# -*- coding: utf-8 -*-

from sqlalchemy.ext.associationproxy import association_proxy
from . import db, TimestampMixin, NodeMixin, Node
from .interface import ConnectionInterface, interface_coupling_table

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
    interfaces = association_proxy('part_interfaces', 'interface', creator=lambda i: PartInterface(interface=i))
    #: TODO: Other metadata such as price

    def is_compatible_with(self, part):
        """
        Do we have an interface that is coupled with one of the interfaces on the other part?
        """
        if isinstance(part, Part):

            # Version 1: local comparison
            # Easy to comprehend, but inefficient because of the loops

            # for li in self.interfaces:
            #     for ri in part.interfaces:
            #         if li in ri.couples:
            #             return True
            # return False

            # Version 2: in-database comparison
            # Provides lesser clarity but offloads heavy lifting to the database

            local_interfaces = [i.id for i in self.interfaces]
            remote_interfaces = [i.id for i in part.interfaces]

            return db.session.query(interface_coupling_table).filter(
                db.or_(
                    db.and_(
                        interface_coupling_table.c.lhs_interface_id.in_(local_interfaces),
                        interface_coupling_table.c.rhs_interface_id.in_(remote_interfaces)),
                    db.and_(
                        interface_coupling_table.c.lhs_interface_id.in_(remote_interfaces),
                        interface_coupling_table.c.rhs_interface_id.in_(local_interfaces))
                    )
                ).first() is not None
        return False


class PartInstance(NodeMixin, Node):
    __tablename__ = 'part_instance'
    part_id = db.Column(None, db.ForeignKey('part.id'))
    part = db.relationship(Part, foreign_keys=[part_id], backref=db.backref('instances', cascade='all, delete-orphan'))
    #: Description of this particular instance (health notes, acquisition story, etc)
    description = db.Column(db.UnicodeText)
    # TODO: Include columns here to describe acquisition date, owner, possessor, etc
