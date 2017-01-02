#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.conf.urls import url
from .views.oauth import oauth_create, oauth_read_or_update_or_delete
from .urls import urlpatterns

urlpatterns += [

    # oAuth2 URLs ------------------------------------

    # ---------------------------------------
    # Read GET
    # Update PUT
    # Delete DELETE
    # ---------------------------------------
    url(r'oauth2/(?P<resource_type>[^/]+)/(?P<id>[^/]+)',
        oauth_read_or_update_or_delete,
        name='monfhir_oauth_read_or_update_or_delete'),

    # create ------------------------------
    url(r'oauth2/(?P<resource_type>[^/]+)', oauth_create,
        name='monfhir_oauth_create'),

]
