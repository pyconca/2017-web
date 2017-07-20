from pyconca2017.pycon_sponsors.services import SponsorsService

from django.template import Template, Context
from django.utils import translation
from test_plus.test import TestCase

from pyconca2017.pycon_sponsors.tests.factories import SponsorFactory, LevelFactory


class TestSponsorService(TestCase):

    def setUp(self):
        self.sut = SponsorsService()
        level1 = LevelFactory(order=2, name_en='One')
        level2 = LevelFactory(order=1, name_en='Two')
        SponsorFactory(level=level1, order=1)
        SponsorFactory(level=level1, order=4)
        SponsorFactory(level=level2, order=3)
        SponsorFactory(level=level2, order=2)

    def test_get_levels_returns_levels(self):
        levels = self.sut.get_levels()
        self.assertEqual(len(levels), 2)

    def test_get_levels_ordered(self):
        levels = self.sut.get_levels().values_list('order', flat=True)
        self.assertEqual(list(levels), [1, 2])

    def test_get_sponsors(self):
        sponsors = self.sut.get_sponsors()
        self.assertEqual(len(sponsors), 4)

    def test_get_sponsors_ordered(self):
        sponsors = self.sut.get_sponsors().values_list('order', flat=True)
        self.assertEqual(list(sponsors), [1, 2, 3, 4])

    def test_get_sponsors_active_only(self):
        SponsorFactory(active=False)
        SponsorFactory(active=False)
        sponsors = self.sut.get_sponsors().values_list('order', flat=True)
        self.assertEqual(len(sponsors), 4)
