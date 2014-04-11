# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid.security import NO_PERMISSION_REQUIRED


@view_config(route_name='home', renderer='/base.jinja2',
             permission=NO_PERMISSION_REQUIRED)
def index_view(request):
    context = {}
    return context
