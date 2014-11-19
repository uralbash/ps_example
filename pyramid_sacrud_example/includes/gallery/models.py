#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Models for gallery
"""

import os

from sqlalchemy import Column, Integer

from pyramid_sqlalchemy import BaseObject as Base

from sacrud.common import TableProperty
from pyramid_sacrud.common.custom import WidgetRelationship

from pyramid_sacrud_gallery.mixins import (
    GalleryMixin, GalleryItemMixin, GalleryItemM2MMixin,
)


upload_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           'static', 'upload')


class TestGallery(GalleryMixin, Base):
    __tablename__ = 'test_gallery'

    pyramid_sacrud_ref_name = 'TestGalleryItem'
    pyramid_sacrud_m2m_table = 'test_gallery_item_m2m'

    id = Column(Integer, primary_key=True)

    @TableProperty
    def sacrud_list_col(cls):
        col = cls.columns
        return [col.name]

    @TableProperty
    def sacrud_detail_col(cls):
        col = cls.columns
        return [('', [col.name,
                      WidgetRelationship(TestGallery.items,
                                         table=TestGalleryItem,
                                         name='Items')])]


class TestGalleryItem(GalleryItemMixin, Base):
    __tablename__ = 'test_gallery_item'

    pyramid_sacrud_ref_name = 'TestGallery'
    pyramid_sacrud_m2m_table = 'test_gallery_item_m2m'
    pyramid_sacrud_upload_path = upload_path

    id = Column(Integer, primary_key=True)

    @TableProperty
    def sacrud_list_col(cls):
        col = cls.columns
        return [col.path, ]

    @TableProperty
    def sacrud_detail_col(cls):
        col = cls.columns
        return [
            ('', [col.image, col.description,
                  WidgetRelationship(TestGalleryItem.galleries,
                                     table=TestGallery,
                                     name='Galleries')]
             )]


class TestGalleryItemM2M(GalleryItemM2MMixin, Base):
    __tablename__ = 'test_gallery_item_m2m'

    pyramid_sacrud_gallery = TestGallery
    pyramid_sacrud_gallery_item = TestGalleryItem
