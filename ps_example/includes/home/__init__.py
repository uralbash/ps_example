#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Home
"""


def includeme(config):
    config.add_jinja2_search_path("templates")
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan('.views')
