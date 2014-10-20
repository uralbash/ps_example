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
from .models.auth import (Company, ExternalIdentity, Group, GroupPermission,
                          GroupResourcePermission, Resource, User, UserGroup,
                          UserPermission, UserResourcePermission)
from .models.postgres import TestHSTORE, TestPostgresTypes
from .models.funny_models import (MPTTPages, TestAllTypes, TestBOOL,
                                  TestCustomizing, TestDeform, TestFile,
                                  TestTEXT, TestUNION)

from .models.catalog import (CatalogCategory, CatalogGroup, CatalogProduct,
                             CatalogStock, Category2Group, Product2Category)


def get_sacrud_models(dialect='sqlite'):
    """ col1 col2 col3
         w1   w4   w7
         w2   w5   w9
         w3
    """
    widgets = {
        'Pages': {
            'tables': [MPTTPages],
            'position': 1,
        },
        '': {
            'tables': [TestTEXT, TestBOOL, TestUNION, TestFile],
            'position': 2,
        },
        'Customizing example': {
            'tables': [TestCustomizing, TestDeform],
            'position': 3,
        },

        'Just for fun': {
            'tables': [TestAllTypes],
            'position': 4,
        },
        'Auth': {
            'tables': [Company, Group, GroupPermission, UserGroup,
                       GroupResourcePermission, Resource, UserPermission,
                       UserResourcePermission, User, ExternalIdentity],
            'position': 5,
        },
    }
    if dialect == 'postgresql':
        widgets['Postgres'] = {
            'tables': [TestHSTORE, TestPostgresTypes],
            'position': 7,
        }
        widgets['Catalog'] = {
            'tables': [CatalogProduct, CatalogCategory, CatalogGroup,
                       CatalogStock, Category2Group, Product2Category],
            'position': 8,
        }
    return widgets
