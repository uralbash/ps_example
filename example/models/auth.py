#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

from pyramid.security import Allow, Authenticated
from sqlalchemy import Column, ForeignKey, Integer, Unicode
from sqlalchemy.orm import relationship
from ziggurat_foundations import ziggurat_model_init
from ziggurat_foundations.models import (ExternalIdentityMixin, GroupMixin,
                                         GroupPermissionMixin,
                                         GroupResourcePermissionMixin,
                                         ResourceMixin, UserGroupMixin,
                                         UserMixin, UserPermissionMixin,
                                         UserResourcePermissionMixin)

from example.models import Base


class Company(Base):
    """ Название мед. учреждения. Например УГМК-Здоровье, Доктор+ итд
    """
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode, nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Group(GroupMixin, Base):
    pass


class GroupPermission(GroupPermissionMixin, Base):
    pass


class UserGroup(UserGroupMixin, Base):
    pass


class GroupResourcePermission(GroupResourcePermissionMixin, Base):
    pass


class Resource(ResourceMixin, Base):
    pass


class UserPermission(UserPermissionMixin, Base):
    pass


class UserResourcePermission(UserResourcePermissionMixin, Base):
    pass


class User(UserMixin, Base):
    """
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode, nullable=False)
    middlename = Column(Unicode, nullable=False)
    surname = Column(Unicode, nullable=False)
    company_id = Column(Integer, ForeignKey(Company.id,
                        onupdate='CASCADE', ondelete='CASCADE'),
                        nullable=False)
    company = relationship('Company')

    def __repr__(self):
        return self.name + ' ' + self.middlename + ' ' + self.surname


class ExternalIdentity(ExternalIdentityMixin, Base):
    pass

ziggurat_model_init(User, Group, UserGroup, GroupPermission, UserPermission,
                    UserResourcePermission, GroupResourcePermission, Resource,
                    ExternalIdentity, passwordmanager=None)

PERMISSION_VIEW = u'view'

class RootFactory(object):
    def __init__(self, request):
        self.__acl__ = [(Allow, Authenticated, PERMISSION_VIEW), ]
        # general page factory - append custom non resource permissions
        # request.user object from cookbook recipie
        if request.user:
            for perm_user, perm_name in request.user.permissions:
                self.__acl__.append((Allow, perm_user, perm_name,))
