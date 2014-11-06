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
from pyramid_sacrud_gallery.views import gallery_view


def includeme(config):
    config.include('pyramid_sacrud_gallery')
    config.add_jinja2_search_path("templates")
    config.add_route('pyramid_sacrud_page_of_gallery', '/admin/gallery/{id}')
    config.add_view(gallery_view,
                    route_name='pyramid_sacrud_page_of_gallery',
                    renderer='pyramid_sacrud_gallery/gallery_sacrud_page.jinja2')
