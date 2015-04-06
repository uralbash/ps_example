#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
RootFactory
"""
from pyramid.security import Allow, Authenticated

PERMISSION_VIEW = 'view'


def get_group_permission_by_user(user):
    group_permissions = []
    for group in user.groups:
        for permission in group.permissions:
            group_permissions.append((user.id, permission.perm_name))
    return group_permissions


class RootFactory(object):

    def __init__(self, request):
        pass

    @property
    def __acl__(self):
        request = self.request
        acl = [(Allow, Authenticated, PERMISSION_VIEW), ]
        if self.request.user:
            group_permissions = get_group_permission_by_user(request.user)
            permissions = request.user.permissions + group_permissions
            for perm_user, perm_name in permissions:
                acl.append((Allow, perm_user, perm_name))
        return acl
