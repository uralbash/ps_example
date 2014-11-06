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
from pyramid_sqlalchemy import BaseObject as Base
from sqlalchemy import Column, Integer

from pyramid_sacrud_gallery.mixins import GalleryItemMixin, GalleryMixin
from sacrud.common import TableProperty


class TestGallery(GalleryMixin, Base):
    __tablename__ = 'test_gallery'

    id = Column(Integer, primary_key=True)

    @TableProperty
    def sacrud_list_col(cls):
        col = cls.columns
        return [col.name]

    @TableProperty
    def sacrud_detail_col(cls):
        col = cls.columns
        return [('', [col.name])]


class TestGalleryItem(GalleryItemMixin, Base):
    __tablename__ = 'test_gallery_item'

    pyramid_sacrud_gallery = TestGallery

    id = Column(Integer, primary_key=True)

    @TableProperty
    def sacrud_list_col(cls):
        col = cls.columns
        return [col.path, col.gallery_id]

    @TableProperty
    def sacrud_detail_col(cls):
        col = cls.columns
        return [('', [col.path, col.description, col.gallery_id])]
