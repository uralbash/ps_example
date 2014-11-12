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
from ..catalog.models import (CatalogCategory, CatalogGroup, CatalogProduct,
                              CatalogStock, Category2Group, Product2Category)
from ..gallery.models import TestGallery, TestGalleryItem
from ..home.models.funny_models import (TestAllTypes, TestBOOL, TestCustomizing,
                                        TestDeform, TestFile, TestTEXT,
                                        TestUNION)
from ..home.models.postgres import TestHSTORE, TestPostgresTypes
from ..pages.models import MPTTPages


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
        'Gallery': {
            'tables': [TestGallery, TestGalleryItem],
            'position': 2,
        },
        '': {
            'tables': [TestTEXT, TestBOOL, TestUNION, TestFile],
            'position': 3,
        },
        'Customizing example': {
            'tables': [TestCustomizing, TestDeform],
            'position': 4,
        },

        'Just for fun': {
            'tables': [TestAllTypes],
            'position': 5,
        },
        'Auth': {
            'tables': [Group, GroupPermission, UserGroup,
                       GroupResourcePermission, Resource, UserPermission,
                       UserResourcePermission, User, ExternalIdentity],
            'position': 6,
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
