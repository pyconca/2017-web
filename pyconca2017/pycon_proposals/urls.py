# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from pyconca2017.pycon_proposals.views import CFPView


urlpatterns = [
    url(r'^$', CFPView.as_view(), name='cfp_main'),
]
