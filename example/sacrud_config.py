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
from example.models.funny_models import (CatalogCategory, CatalogGroup,
                                         CatalogProduct, CatalogStock,
                                         Category2Group, MPTTPages,
                                         Product2Category, TestAllTypes,
                                         TestBOOL, TestCustomizing, TestFile,
                                         TestHSTORE, TestTEXT, TestUNION,
                                         WidgetPosition)


def get_sacrud_models():
    """ col1 col2 col3
         w1   w2   w3
         w4   w5   w6
         w7   w8   w9
    """
    return {
        # Column 1
        'Postgres': {
            'tables': [TestHSTORE],
            'position': 1,
        },
        '': {
            'tables': [TestTEXT, TestBOOL, TestUNION, TestFile],
            'position': 4,
        },
        'Just for fun': {
            'tables': [TestAllTypes],
            'position': 7,
        },

        # Column 2
        'Customizing example': {
            'tables': [TestCustomizing, WidgetPosition],
            'position': 2,
        },
        'Pages': {
            'tables': [MPTTPages],
            'position': 5,
        },
        'Auth': {
            'tables': [Company, Group, GroupPermission, UserGroup,
                       GroupResourcePermission, Resource, UserPermission,
                       UserResourcePermission, User, ExternalIdentity],
            'position': 8,
        },

        # Column 3
        'Catalog': {
            'tables': [CatalogProduct, CatalogCategory, CatalogGroup,
                       CatalogStock, Category2Group, Product2Category],
            'position': 3,
        },
    }
