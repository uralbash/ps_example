#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
List of models for pyramid_sacrud
"""
from ..auth.models import (ExternalIdentity, Group, GroupPermission,
                           GroupResourcePermission, Resource, User, UserGroup,
                           UserPermission, UserResourcePermission)
from ..home.models.funny_models import (TestAllTypes, TestBOOL,
                                        TestCustomizing, TestDeform, TestFile,
                                        TestTEXT, TestUNION)
from ..home.models.postgres import TestHSTORE, TestPostgresTypes
from ..pages.models import MPTTPages


def get_sacrud_models(dialect='sqlite'):
    """ col1 col2 col3
         w1   w2   w3
         w4   w5
    """
    widgets = [
        ('Pages', [MPTTPages]),
        ('', [TestTEXT, TestBOOL, TestUNION, TestFile]),
        ('Customizing example', [TestCustomizing, TestDeform]),
        ('Just for fun', [TestAllTypes]),
        ('Auth', [Group, GroupPermission, UserGroup,
                  GroupResourcePermission, Resource, UserPermission,
                  UserResourcePermission, User, ExternalIdentity])
    ]
    if dialect == 'postgresql':
        widgets.append(('Postgres', [TestHSTORE, TestPostgresTypes]))
    return widgets
