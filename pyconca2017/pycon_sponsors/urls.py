# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from pyconca2017.pycon_sponsors.views import SponsorsPageView

urlpatterns = [
    url(r'^$', SponsorsPageView.as_view(), name='sponsors'),
]
