#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Auth models
"""
from pyramid_sqlalchemy import BaseObject
from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.orm import relationship
from ziggurat_foundations import ziggurat_model_init
from ziggurat_foundations.models import (ExternalIdentityMixin, GroupMixin,
                                         GroupPermissionMixin,
                                         GroupResourcePermissionMixin,
                                         ResourceMixin, UserGroupMixin,
                                         UserMixin, UserPermissionMixin,
                                         UserResourcePermissionMixin)

from sacrud.common import TableProperty


class User(UserMixin, BaseObject):
    verbose_name = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode, nullable=False)
    middlename = Column(Unicode, nullable=False)
    surname = Column(Unicode, nullable=False, default=1)

    def __repr__(self):
        return self.name + ' ' + self.middlename + ' ' + self.surname

    # SACRUD
    @TableProperty
    def sacrud_detail_col(cls):
        col = cls.columns
        return [('', [col.user_name, col.email, col.user_password]),
                ('personal data', [col.name, col.middlename, col.surname])]


class UserPermission(UserPermissionMixin, BaseObject):
    verbose_name = 'Permissions of user'

    user = relationship('User')


class Group(GroupMixin, BaseObject):
    verbose_name = 'Group'

    def __repr__(self):
        return self.group_name


class GroupPermission(GroupPermissionMixin, BaseObject):
    verbose_name = 'Permissions of group'


class UserGroup(UserGroupMixin, BaseObject):
    verbose_name = 'Users of group'

    user = relationship('User')
    group = relationship('Group')


class Resource(ResourceMixin, BaseObject):
    verbose_name = 'Resource'

    parent = relationship('Resource')
    owner_group = relationship('Group')


class GroupResourcePermission(GroupResourcePermissionMixin, BaseObject):
    pass


class UserResourcePermission(UserResourcePermissionMixin, BaseObject):
    pass


class ExternalIdentity(ExternalIdentityMixin, BaseObject):
    pass

ziggurat_model_init(User, Group, UserGroup, GroupPermission, UserPermission,
                    UserResourcePermission, GroupResourcePermission, Resource,
                    ExternalIdentity, passwordmanager=None)
