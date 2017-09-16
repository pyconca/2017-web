# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from pyconca2017.pycon_schedule.views import ScheduleView, ScheduleRedirectView

urlpatterns = [
    url(r'^$', ScheduleRedirectView.as_view(), name='current'),
    url(r'^(?P<schedule_date>\d{4}-\d{2}-\d{2})$', staff_member_required(ScheduleView.as_view()), name='detail'),
]
