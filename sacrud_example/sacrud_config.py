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
from .models.funny_models import (CatalogCategory, CatalogGroup, CatalogProduct,
                                  CatalogStock, Category2Group, MPTTPages,
                                  Product2Category, TestAllTypes, TestBOOL,
                                  TestCustomizing, TestDeform, TestFile,
                                  TestHSTORE, TestTEXT, TestUNION)


def get_sacrud_models():
    """ col1 col2 col3
         w1   w4   w7
         w2   w5   w9
         w3
    """
    return {
        # Column 1
        'Postgres': {
            'tables': [TestHSTORE],
            'position': 1,
        },
        'Customizing example': {
            'tables': [TestCustomizing, TestDeform],
            'position': 2,
        },
        'Catalog': {
            'tables': [CatalogProduct, CatalogCategory, CatalogGroup,
                       CatalogStock, Category2Group, Product2Category],
            'position': 3,
        },

        # Column 2
        '': {
            'tables': [TestTEXT, TestBOOL, TestUNION, TestFile],
            'position': 4,
        },
        'Pages': {
            'tables': [MPTTPages],
            'position': 5,
        },

        # Column 3
        'Just for fun': {
            'tables': [TestAllTypes],
            'position': 7,
        },
        'Auth': {
            'tables': [Company, Group, GroupPermission, UserGroup,
                       GroupResourcePermission, Resource, UserPermission,
                       UserResourcePermission, User, ExternalIdentity],
            'position': 8,
        },
    }
