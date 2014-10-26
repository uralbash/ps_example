# -*- coding: utf-8 -*-
from pyramid.events import BeforeRender, subscriber
from pyramid.view import notfound_view_config
from pyramid_sqlalchemy import Session as DBSession

from pyramid_sacrud_pages.common import get_pages_menu

from ..models.funny_models import MPTTPages


def get_menu(**kwargs):
    return get_pages_menu(DBSession, MPTTPages, **kwargs)


@subscriber(BeforeRender)
def add_global(event):
    event['page_menu'] = get_menu


@notfound_view_config(append_slash=True, renderer='404.jinja2')
def notfound(request):
    request.response.status = 404
    return {}
