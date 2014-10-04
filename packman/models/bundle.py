# -*- coding: utf-8 -*-

from . import db, NodeMixin, Node, make_timestamp_columns
from .part import Part

__all__ = ['BundleSpec', 'Bundle']


bundlespec_part_table = db.Table('bundlespec_part', db.Model.metadata,
    *(make_timestamp_columns() + (
        db.Column('bundlespec_id', None, db.ForeignKey('bundlespec.id'), primary_key=True),
        db.Column('part_id', None, db.ForeignKey('part.id'), primary_key=True)
        )))


class BundleSpec(NodeMixin, Node):
    """
    A reference specification for bundles, to record the original contents of a retail package
    or the ideal set of parts required to perform a task.
    """
    __tablename__ = 'bundlespec'
    parts = db.relationship(Part, secondary=bundlespec_part_table, order_by=Part.title)


class Bundle(NodeMixin, Node):
    """
    A bundle of parts, as it currently exists, to help move them around together.
    """
    __tablename__ = 'bundle'
    description = db.Column(db.UnicodeText)
    bundlespec_id = db.Column(None, db.ForeignKey('bundlespec.id'), nullable=True)
    bundlespec = db.relationship(BundleSpec, foreign_keys=[bundlespec_id], backref='bundles')
