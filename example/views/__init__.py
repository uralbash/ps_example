# -*- coding: utf-8 -*-
from pyramid.view import view_config


@view_config(route_name='home', renderer='/base.jinja2', permission='view')
def index_view(request):
    context = {}
    return context
