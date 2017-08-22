
from django.db.models import Count
from pyconca2017.pycon_sponsors.models import PySponsor, PySponsorLevel


class SponsorsService(object):

    def get_sponsors(self):
        """ Get active sponsors to show on the website """
        return PySponsor.objects.filter(
            active=True
        ).order_by(
            'level__order', 'order'
        )

    def get_levels(self):

        return PySponsorLevel.objects.annotate(sponsor_count=Count('py_sponsors')).filter(sponsor_count__gt=0).order_by('order')
