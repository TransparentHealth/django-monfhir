#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.conf.urls import include, url
from .views.create import create
from .views.rud import read_or_update_or_delete
from .views.search import search
from .views.history import history, vread
from .views.hello import hello

urlpatterns = [

    # Hello
    url(r'hello', hello,
        name='monfhir_hello'),


    # URLs with no authentication
    # Interactions on Resources
    # Vread GET --------------------------------
    url(r'(?P<resource_type>[^/]+)/(?P<id>[^/]+)/_history/(?P<vid>[^/]+)', vread,
        name='monfhir_vread'),

    # History GET ------------------------------
    url(r'(?P<resource_type>[^/]+)/(?P<id>[^/]+)/_history', history,
        name='monfhir_history'),

    # ---------------------------------------
    # Read GET
    # Update PUT
    # Delete DELETE
    # ---------------------------------------
    url(r'(?P<resource_type>[^/]+)/(?P<id>[^/]+)',
        read_or_update_or_delete,
        name='monfhir_read_or_update_or_delete'),


    # Create  POST ------------------------------
    url(r'(?P<resource_type>[^/]+)', create,
        name='monfhir_create'),

    # Search  GET ------------------------------
    url(r'(?P<resource_type>[^/]+)?', search,
        name='monfhir_search'),


]
