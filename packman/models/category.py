# -*- coding: utf-8 -*-

from . import db, NodeMixin, Node, make_timestamp_columns
from .interface import ConnectionInterface
from .part import Part

__all__ = ['Category']


category_interface_table = db.Table('category_interface', db.Model.metadata,
    *(make_timestamp_columns() + (
        db.Column('category_id', None, db.ForeignKey('category.id'), primary_key=True),
        db.Column('interface_id', None, db.ForeignKey('interface.id'), primary_key=True)
        )))


category_part_table = db.Table('category_part', db.Model.metadata,
    *(make_timestamp_columns() + (
        db.Column('category_id', None, db.ForeignKey('category.id'), primary_key=True),
        db.Column('part_id', None, db.ForeignKey('part.id'), primary_key=True)
        )))


class Category(NodeMixin, Node):
    __tablename__ = 'category'
    description = db.Column(db.UnicodeText)
    interfaces = db.relationship(ConnectionInterface, secondary=category_interface_table, order_by=ConnectionInterface.title)
    parts = db.relationship(Part, secondary=category_part_table, order_by=Part.title)
