# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include

import symposion.views

from pyconca2017.pycon_proposals.views import CFPView, submit_proposal


urlpatterns = [
    url(r'^$', CFPView.as_view(), name='cfp_main'),
    url(r'^submit_proposal/$', submit_proposal, name='submit_talk_proposal'),


    url(r"^dashboard/", symposion.views.dashboard, name="dashboard"),
    url(r"^speaker/", include("symposion.speakers.urls")),
    url(r"^proposals/", include("symposion.proposals.urls")),
    url(r"^sponsors/", include("symposion.sponsorship.urls")),
    url(r"^teams/", include("symposion.teams.urls")),
    url(r"^reviews/", include("symposion.reviews.urls")),
    url(r"^schedule/", include("symposion.schedule.urls")),
]
