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
from pyramid_sacrud_catalog.models import (BaseCategory, BaseGroup, BaseProduct,
                                           BaseStock, Category2Group,
                                           Product2Category, Product2Group)

from sacrud.common import TableProperty
from pyramid_sacrud.common.custom import WidgetM2M
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CatalogProduct(Base, BaseProduct):

    @TableProperty
    def sacrud_detail_col(cls):
        model = CatalogProduct
        return [('', [model.name, model.visible,
                      WidgetM2M(column=model.category),
                      WidgetM2M(column=model.group),
                      model.params]),
                ]


class CatalogCategory(BaseCategory, Base):

    @TableProperty
    def sacrud_detail_col(cls):
        model = CatalogCategory
        return [('', [model.name, model.visible, model.abstract,
                      WidgetM2M(column=model.group,
                                name='group')]),
                ]


class CatalogGroup(BaseGroup, Base):

    @TableProperty
    def sacrud_detail_col(cls):
        model = CatalogGroup
        return [('', [model.name, model.visible,
                      WidgetM2M(column=model.category)]),
                ]


class CatalogStock(BaseStock, Base):
    pass


class Category2Group(Category2Group, Base):
    pass


class Product2Category(Product2Category, Base):
    pass


class Product2Group(Product2Group, Base):
    pass
