#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Anykey for sacrud
"""
from example.models.auth import (Company, ExternalIdentity, Group,
                                 GroupPermission, GroupResourcePermission,
                                 Resource, User, UserGroup, UserPermission,
                                 UserResourcePermission)
from example.models.funny_models import (MPTTPages, TestAllTypes, TestBOOL,
                                         TestCustomizing, TestDND, TestFile,
                                         TestHSTORE, TestTEXT, TestUNION,
                                         WidgetPosition)


def get_sacrud_models():
    # Columns and positions start at 0
    return {
        'Postgres': {
            'tables': [TestHSTORE],
        },
        '': {
            'tables': [TestTEXT, TestBOOL, TestDND, TestUNION, TestFile],
        },
        'Just for fun': {
            'tables': [TestAllTypes],
            'column': 1,
            'position': 0,
        },
        'Customizing example': {
            'tables': [TestCustomizing, WidgetPosition],
            'column': 1,
            'position': 1,
        },
        'Pages': {
            'tables': [MPTTPages],
            'column': 2,
            'position': 0,
        },
        'Auth': {
            'tables': [Company, Group, GroupPermission, UserGroup,
                       GroupResourcePermission, Resource, UserPermission,
                       UserResourcePermission, User, ExternalIdentity],
            'column': 2,
            'position': 1,
        },
    }
