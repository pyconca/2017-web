from test_plus.test import TestCase

from pyconca2017.pycon_sponsors.tests.factories import LevelFactory, SponsorFactory


class TestSponsor(TestCase):

    def test__str__(self):
        self.assertEqual(str(SponsorFactory()), 'Demo EN')

    def test_twitter_url_en(self):
        self.assertEqual(SponsorFactory().twitter_url_en, 'https://twitter.com/demo_en')

    def test_twitter_url_fr(self):
        self.assertEqual(SponsorFactory().twitter_url_fr, 'https://twitter.com/demo_fr')

    def test_twitter_url_en_none(self):
        sponsor = SponsorFactory(twitter_username_en=None)
        self.assertEqual(sponsor.twitter_url_en, None)

    def test_twitter_url_fr_none(self):
        sponsor = SponsorFactory(twitter_username_fr=None)
        self.assertEqual(sponsor.twitter_url_fr, None)


class TestSponsorLevel(TestCase):

    def setUp(self):
        self.level = LevelFactory()
        SponsorFactory(level=self.level, order=2, active=False)
        SponsorFactory(level=self.level, order=3)
        SponsorFactory(level=self.level, order=1)

    def test__str__(self):
        self.assertEqual(str(self.level), 'Gold')

    def test_sponsors_active_only(self):
        sponsors = self.level.sponsors()
        self.assertEqual(len(sponsors), 2)

    def test_sponsors_order(self):
        sponsors = self.level.sponsors().values_list('order', flat=True)
        self.assertEqual(list(sponsors), [1, 3])
