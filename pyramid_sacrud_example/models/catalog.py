#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Models for catalog of products
"""
from pyramid_sacrud_catalog.models import (BaseCategory, BaseGroup, BaseStock,
                                           BaseProduct, Category2Group,
                                           Product2Category, Product2Group)

from sacrud.common import TableProperty
from pyramid_sacrud.common.custom import WidgetRelationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CatalogProduct(Base, BaseProduct):

    @TableProperty
    def sacrud_detail_col(cls):
        model = CatalogProduct
        category_m2m = WidgetRelationship(relation=model.category, table=model,
                                          name='categories')
        groups_m2m = WidgetRelationship(relation=model.group, table=model,
                                        name='groups')
        fields_groups_list = [
            ('Fields group name', [model.name, model.visible, category_m2m,
                                   groups_m2m, model.params]),
        ]
        return fields_groups_list


class CatalogCategory(BaseCategory, Base):

    @TableProperty
    def sacrud_detail_col(cls):
        model = CatalogCategory
        groups_m2m = WidgetRelationship(relation=model.group, table=model,
                                        name='group')
        return [('', [model.name, model.visible, model.abstract, groups_m2m])]


class CatalogGroup(BaseGroup, Base):

    @TableProperty
    def sacrud_detail_col(cls):
        model = CatalogGroup
        category_m2m = WidgetRelationship(relation=model.category, table=model,
                                          name='categories')
        return [('', [model.name, model.visible, category_m2m])]


class CatalogStock(BaseStock, Base):
    pass


class Category2Group(Category2Group, Base):
    pass


class Product2Category(Product2Category, Base):
    pass


class Product2Group(Product2Group, Base):
    pass
