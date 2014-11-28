#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Gallery
"""


def includeme(config):
    config.add_jinja2_search_path("templates")
    config.include('pyramid_sacrud_gallery')
    config.include('.page_of_sacrud')
    config.add_static_view('static_sacrud_gallery', 'static', cache_max_age=3600)
