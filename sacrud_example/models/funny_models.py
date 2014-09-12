#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Models for example
"""
import os
import uuid

from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime, Enum,
                        Float, ForeignKey, Integer, Numeric, String, Text,
                        Unicode, UnicodeText)
from sqlalchemy.dialects.postgresql import ARRAY, BYTEA, HSTORE, JSON
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship

from pyramid_sacrud.common.custom import widget_link, widget_m2m
from pyramid_sacrud_catalog.models import (BaseCategory, BaseGroup, BaseProduct,
                                           BaseStock, Category2Group,
                                           Product2Category, Product2Group)
from pyramid_sacrud_pages.models import BasePages
from sacrud.common import TableProperty
from sacrud.exttype import ChoiceType, ElfinderString, FileStore, GUID, SlugType

from ..models import Base

file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..',
                         'static')


class TestDeform(Base):
    __tablename__ = "test_deform"

    id = Column(Integer, primary_key=True)
    hstore = Column(MutableDict.as_mutable(HSTORE))
    filestore = Column(FileStore(path="/static/uploaded/",
                                 abspath=os.path.join(file_path, 'uploaded')))
    filestore2 = Column(FileStore(path="/static/uploaded/",
                                  abspath=os.path.join(file_path, 'uploaded')))
    filestore3 = Column(FileStore(path="/static/uploaded/",
                                  abspath=os.path.join(file_path, 'uploaded')))

    TEST_CHOICES = (
        ('OK (200)', '200'),
        ('Moved Permanently (301)', '301'),
        ('Moved Temporarily (302)', '302'),
    )

    choice = Column(ChoiceType(choices=TEST_CHOICES))
    guid = Column(GUID(), default=uuid.uuid4)
    json = Column(JSON)  # for postgresql 9.3 version
    enum = Column(Enum(u'IPv6', u'IPv4', name=u"ip_type"))

    elfinder = Column(ElfinderString,
                      info={"verbose_name": u'Проверка Elfinder', })

    foo = Column(String)
    slug = Column(SlugType('foo', False))


class TestHSTORE(Base):

    """
    SQLAlchemy model for demonstration of the postgres dialect
    :class:`sqlalchemy.dialects.postgresql.HSTORE` field

    :param id: standart pk.
    :param foo: :class:`sqlalchemy.dialects.postgresql.HSTORE` field.

    Usage::

        >>> hash = {'param1': 'foo', 'param2': 'bar'}
        >>> hstore_obj = TestHSTORE(hash)
        >>> hstore_obj.foo
        {'param2': 'bar', 'param1': 'foo'}

    """
    __tablename__ = 'test_hstore'

    id = Column(Integer, primary_key=True)
    foo = Column(MutableDict.as_mutable(HSTORE),
                 nullable=False, unique=True)

    def __init__(self, foo):
        self.foo = foo


class TestFile(Base):

    """
    SQLAlchemy model for demonstration file field.
    """
    __tablename__ = 'test_file'

    id = Column(Integer, primary_key=True)
    image = Column(FileStore(path="/static/uploaded/",
                             abspath=os.path.join(file_path, 'uploaded')))

    def __init__(self, image):
        self.image = image


class TestTEXT(Base):

    """
    SQLAlchemy model for demonstration work with any text type field.

    :param id: standart pk.
    :param foo: :class:`sqlalchemy.String` field.
    :param ufoo: :class:`sqlalchemy.Unicode` field.
    :param fooText: :class:`sqlalchemy.Text` field.
    :param ufooText: :class:`sqlalchemy.UnicodeText` field.

    Usage::

        >>> params = ('blablabla', 'blablabla!', 'bla bla bla', 'blablabla')
        >>> text_obj = TestTEXT(*params)
        >>> text_obj.foo, text_obj.ufoo, text_obj.fooText, text_obj.ufooText
        ('blablabla', 'blablabla!', 'bla bla bla', 'blablabla')

    """
    __tablename__ = 'test_text'
    __mapper_args__ = {'order_by': 'id'}

    id = Column(Integer, primary_key=True)
    foo = Column(String)
    ufoo = Column(Unicode)
    fooText = Column(Text)
    ufooText = Column(UnicodeText)

    def __init__(self, foo, ufoo, fooText, ufooText):
        self.foo = foo
        self.ufoo = ufoo
        self.fooText = fooText
        self.ufooText = ufooText

    # SACRUD
    verbose_name = 'test_text and pagination'


class TestBOOL(Base):

    """
    SQLAlchemy model for demonstration :class:`sqlalchemy.Boolean` field

    :param id: standart pk.
    :param foo: :class:`sqlalchemy.Boolean` field.

    Usage::

        >>> TestBOOL(True).foo, TestBOOL(False).foo
        (True, False)

    """
    __tablename__ = 'test_bool'

    id = Column(Integer, primary_key=True)
    foo = Column(Boolean)

    def __init__(self, foo):
        self.foo = foo


class TestUNION(Base):

    """
    SQLAlchemy model for demonstration union field.

    :param id: standart pk.
    :param name: :class:`sqlalchemy.Unicode` field.
    :param foo: :class:`sqlalchemy.Boolean` field.
    :param double_cash: :class:`sqlalchemy.Numeric` field.
    """
    __tablename__ = 'test_union'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    foo = Column(Boolean)
    cash = Column(Integer)
    double_cash = Column(Numeric(10, 2))

    def __init__(self, name, foo, cash, double_cash):
        self.name = name
        self.foo = foo
        self.cash = cash
        self.double_cash = double_cash

    def __repr__(self):
        return self.name


class TestAllTypes(Base):

    """
    SQLAlchemy model for demonstration all types field.
    """
    __tablename__ = 'test_alltypes'

    TEST_CHOICES = {'val_1': 'val_1', 'val_2': 'val_2', 'val_3': 'val_3',
                    'val_4': 'val_4', 'val_5': 'val_5', 'val_6': 'val_6'}

    col_pk = Column(Integer, primary_key=True)
    col_array = Column(ARRAY(Integer, as_tuple=True))
    col_bigint = Column(BigInteger)
    col_boolean = Column(Boolean)
    col_date_time = Column(Date)
    col_date = Column(DateTime)
    col_date2 = Column(DateTime)
    col_enum = Column(Enum(u'IPv6', u'IPv4', name=u"ip_type"))
    col_choice = Column(ChoiceType(choices=TEST_CHOICES),
                        info={"verbose_name": u'Проверка select', })
    col_float = Column(Float)

    # http://sqlalchemy.readthedocs.org/en/latest/orm/relationships.html?highlight=remote_side#adjacency-list-relationships
    fk_test_alltypes = Column(Integer, ForeignKey('test_alltypes.col_pk'))
    fk_test_union = Column(Integer, ForeignKey('test_union.id'))
    testalltypes = relationship('TestAllTypes')
    testunion = relationship('TestUNION')

    col_elfinder = Column(ElfinderString, info={"verbose_name": u'Проверка Elfinder', })

    col_guid = Column(GUID(), default=uuid.uuid4)
    col_hstore = Column(MutableDict.as_mutable(HSTORE))
    col_integer = Column(Integer)

    col_json = Column(JSON)  # for postgresql 9.3 version
    col_numeric = Column(Numeric(10, 2))
    col_string = Column(String)
    col_text = Column(Text)
    col_unicode = Column(Unicode)
    col_unicode_text = Column(UnicodeText)

    sak = Column(BYTEA, default="FF")

    def __repr__(self):
        return self.col_pk


class TestCustomizing(Base):
    __tablename__ = "test_customizing"

    id = Column(Integer, primary_key=True)
    name = Column(String, info={"description": "put there name"})
    date = Column(Date, info={"verbose_name": 'date JQuery-ui'})
    name_ru = Column(String, info={"verbose_name": u'Название', })
    name_fr = Column(String, info={"verbose_name": u'nom', })
    name_bg = Column(String, info={"verbose_name": u'Име', })
    name_cze = Column(String, info={"verbose_name": u'název', })
    description = Column(Text)
    description2 = Column(Text)

    visible = Column(Boolean)
    in_menu = Column(Boolean, info={"verbose_name": u'menu?',
                                    "description": "Added this page in menu"})
    in_banner = Column(Boolean, info={"verbose_name": u'on banner?', })

    # SACRUD
    verbose_name = u'Customizing table'
    sacrud_css_class = {'tinymce': [description, description2],
                        'content': [description],
                        'name': [name], 'Date': [date]}
    sacrud_list_col = [widget_link(column=name, sacrud_name=u'name'), name_ru, name_cze]
    sacrud_detail_col = [('name space', [name,
                                         ('i18 names', (name_ru, name_bg,
                                                        name_fr, name_cze)
                                          )]
                          ),
                         ('description', [description, date,
                                          (u"Расположение",
                                           (in_menu, visible, in_banner)
                                           ),
                                          description2])
                         ]
    # Sacrud search
    sacrud_search_col = [name]

"""
        PAGES here
"""


class MPTTPages(BasePages, Base):
    __tablename__ = "mptt_pages"

    id = Column(Integer, primary_key=True)

    @TableProperty
    def sacrud_list_col(cls):
        col = cls.columns
        return [col.name, col.level, col.tree_id,
                col.parent_id, col.left, col.right]

    @TableProperty
    def sacrud_detail_col(cls):
        col = cls.columns
        return [('', [col.name, col.slug, col.description, col.visible,
                      col.in_menu, col.parent_id]),
                ('Redirection', [col.redirect_url, col.redirect_page,
                                 col.redirect_type]),
                ('SEO', [col.seo_title, col.seo_keywords, col.seo_description,
                         col.seo_metatags])
                ]

"""
        CATALOG of product here
"""


class CatalogProduct(Base, BaseProduct):

    @TableProperty
    def sacrud_detail_col(cls):
        model = CatalogProduct
        return [('', [model.name, model.visible,
                      widget_m2m(column=model.category),
                      widget_m2m(column=model.group),
                      model.params]),
                ]


class CatalogCategory(BaseCategory, Base):

    @TableProperty
    def sacrud_detail_col(cls):
        model = CatalogCategory
        return [('', [model.name, model.visible, model.abstract,
                      widget_m2m(column=model.group)]),
                ]


class CatalogGroup(BaseGroup, Base):

    @TableProperty
    def sacrud_detail_col(cls):
        model = CatalogGroup
        return [('', [model.name, model.visible,
                      widget_m2m(column=model.category)]),
                ]


class CatalogStock(BaseStock, Base):
    pass


class Category2Group(Category2Group, Base):
    pass


class Product2Category(Product2Category, Base):
    pass


class Product2Group(Product2Group, Base):
    pass
