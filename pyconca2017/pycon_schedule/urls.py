# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from pyconca2017.pycon_schedule.views import ScheduleView, ScheduleRedirectView, PresentationView, AssignFromCSVView

urlpatterns = [
    url(r'^$', ScheduleRedirectView.as_view(), name='current'),
    url(r'^(?P<schedule_date>\d{4}-\d{2}-\d{2})$',
        ScheduleView.as_view(), name='detail'),
    url(r'^(?P<presentation_pk>\d+)/$', PresentationView.as_view(), name='presentation'),
    url(r'^assign_from_csv$', AssignFromCSVView.as_view(), name='assign-from-csv'),
]
