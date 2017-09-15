# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from pyconca2017.pycon_schedule.views import SchedulePreview

urlpatterns = [
    url(r'^preview$', staff_member_required(SchedulePreview.as_view()), name='preview'),
]
