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
from sqlalchemy.dialects.postgresql import ARRAY, HSTORE  # JSON,
from sqlalchemy.event import listen
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship

from example.models import Base
from sacrud.common.custom import as_link, horizontal_field
from sacrud.common.sa_helpers import TableProperty
from sacrud.exttype import FileStore, GUID, ChoiceType
from sacrud.position import before_insert
from sacrud_catalog.models import (BaseCategory, BaseGroup, BaseProduct,
                                   BaseStock)
from sacrud_pages.models import BasePages

file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..',
                         'static')


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


class TestDND(Base):

    """
    SQLAlchemy model for demonstration draggable field.

    :param id: standart pk.
    :param name: :class:`sqlalchemy.Unicode` field.
    :param value: :class:`sqlalchemy.Integer` field.
    :param position1: :class:`sqlalchemy.Integer` field.
    """
    __tablename__ = 'test_dnd'
    __mapper_args__ = {'order_by': 'position1'}

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    value = Column(Integer)
    position1 = Column(Integer, default=0)

    def __init__(self, name, value, position1):
        self.name = name
        self.value = value
        self.position1 = position1

listen(TestDND, "before_insert", before_insert)
listen(TestDND, "before_update", before_insert)


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

    col_guid = Column(GUID(), default=uuid.uuid4)
    col_hstore = Column(MutableDict.as_mutable(HSTORE))
    col_integer = Column(Integer)
    # for postgresql 9.3 version
    # col_json = Column(JSON)
    col_numeric = Column(Numeric(10, 2))
    col_string = Column(String)
    col_text = Column(Text)
    col_unicode = Column(Unicode)
    col_unicode_text = Column(UnicodeText)

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
    sacrud_list_col = [as_link(name, sacrud_name=u'name'), name_ru, name_cze]
    sacrud_detail_col = [('name space', [name,
                                         horizontal_field(name_ru, name_bg,
                                                          name_fr, name_cze,
                                                          sacrud_name=u"i18n names")]),
                         ('description', [description, date,
                                          horizontal_field(in_menu, visible,
                                                           in_banner,
                                                           sacrud_name=u"Расположение"),
                                          description2])
                         ]


class WidgetPosition(Base):
    """SACRUD main page widgets position"""

    __tablename__ = "widget_position"

    id = Column(Integer, primary_key=True)
    widget = Column(String)
    column = Column(Integer)
    position = Column(Integer)

    __mapper_args__ = {'order_by': [column, position]}


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
                      col.in_menu]),
                ('Redirection', [col.redirect_url, col.redirect_page,
                                 col.redirect_type]),
                ('SEO', [col.seo_title, col.seo_keywords, col.seo_description,
                         col.seo_metatags])
                ]

MPTTPages.register_tree()


class CatalogProduct(Base, BaseProduct):
    pass


class CatalogCategory(Base, BaseCategory):
    pass


class CatalogGroup(Base, BaseGroup):
    pass


class CatalogStock(Base, BaseStock):
    pass
