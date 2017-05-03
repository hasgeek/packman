# -*- coding: utf-8 -*-

from collections import defaultdict
from sqlalchemy.ext.associationproxy import association_proxy
from . import db, NodeMixin, Node, TimestampMixin
from .part import Part, PartInstance

__all__ = ['Bundlespec', 'Bundle']


class BundlespecPart(TimestampMixin, db.Model):
    __tablename__ = 'bundlespec_part'
    bundlespec_id = db.Column(None, db.ForeignKey('bundlespec.id'), primary_key=True)
    part_id = db.Column(None, db.ForeignKey('part.id'), primary_key=True)
    part = db.relationship(Part, backref=db.backref('specparts', cascade='all, delete-orphan'))
    count = db.Column(db.Integer, nullable=False, default=1)


class Bundlespec(NodeMixin, Node):
    """
    A reference specification for bundles, to record the original contents of a retail package
    or the ideal set of parts required to perform a task.
    """
    __tablename__ = 'bundlespec'
    specparts = db.relationship(BundlespecPart, backref='bundlespec', cascade='all, delete-orphan')
    parts = association_proxy('specparts', 'part', creator=lambda p: BundlespecPart(part=p))
    frozen = db.Column(db.Boolean, nullable=False, default=False)


class Bundle(NodeMixin, Node):
    """
    A bundle of parts, as it currently exists, to help move them around together.
    """
    __tablename__ = 'bundle'
    description = db.Column(db.UnicodeText)
    bundlespec_id = db.Column(None, db.ForeignKey('bundlespec.id'), nullable=True)
    bundlespec = db.relationship(Bundlespec, foreign_keys=[bundlespec_id], backref='bundles')

    def make_spec(self, replace=False):
        """
        Convert this bundle into a spec.
        """
        # Do we have a bundlespec? If not, make a new one.
        if self.bundlespec and not self.bundlespec.frozen and replace is False:
            bundlespec = self.bundlespec
        else:
            bundlespec = Bundlespec(title=self.title, parent=self.parent)
            self.bundlespec = bundlespec

        # Track parts and their counts
        partcounts = defaultdict(int)

        # Recurse through the node tree looking for part instances and count the parts referred to
        def get_part_counts(node):
            for item in node.nodes.values():
                if isinstance(item, PartInstance):
                    partcounts[item.part] += 1
                get_part_counts(item)  # Recurse through sub-nodes looking for part instances
        get_part_counts(self)

        # Track spec parts that are no longer in the instance
        remove_specparts = []

        # Sync partcounts with the bundlespec
        for specpart in bundlespec.specparts:
            if specpart.part in partcounts:
                specpart.count = partcounts.pop(specpart.part)
            else:
                remove_specparts.append(specpart)

        # Remove the specparts that are no longer in the bundle instance
        for specpart in remove_specparts:
            bundlespec.specparts.remove(specpart)

        # Add the new parts that are in the bundle instance but not the spec
        for part in partcounts:
            bundlespec.specparts.append(BundlespecPart(part=part, count=partcounts[part]))

        return bundlespec
