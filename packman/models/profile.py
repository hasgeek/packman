# -*- coding: utf-8 -*-

from flask_lastuser.sqlalchemy import ProfileMixin
from . import NodeMixin, Node

__all__ = ['Profile']


class Profile(ProfileMixin, NodeMixin, Node):
    """
    Profiles are linked to users and organizations and serve as the parent
    nodes for each user/organization's tree of categories, locations, bundles
    and parts (both specs and instances).

    Profiles are not root nodes. They all exist under a global root node.
    """
    __tablename__ = 'profile'
