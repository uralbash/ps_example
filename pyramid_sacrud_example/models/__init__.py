#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.
import ziggurat_foundations.models
from pyramid_sqlalchemy import Session

ziggurat_foundations.models.DBSession = Session
