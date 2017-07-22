from django.template import Template, Context
from django.utils import translation
from test_plus.test import TestCase

from pyconca2017.pycon_sponsors.tests.factories import SponsorFactory


class TestBilingualTags(TestCase):

    def setUp(self):
        translation.activate('en')
        self.sponsor = SponsorFactory()
        self.template = Template("{% load bilingual %}{% bilingual obj 'name' %}")

    def test_renders_english(self):
        rendered = self.template.render(Context({'obj': self.sponsor}))
        self.assertEqual(rendered, 'Demo EN')

    def test_renders_french(self):
        translation.activate('fr')
        rendered = self.template.render(Context({'obj': self.sponsor}, ))
        self.assertEqual(rendered, 'Demo FR')

    def test_renders_defaults_to_english(self):
        translation.activate('fr')
        sponsor = SponsorFactory(twitter_username_fr=None)
        template = Template("{% load bilingual %}{% bilingual obj 'twitter_username' %}")
        rendered = template.render(Context({'obj': sponsor}, ))
        self.assertEqual(rendered, 'demo_en')

    def test_renders_invalid_field(self):
        template = Template("{% load bilingual %}{% bilingual obj 'foobar' %}")
        rendered = template.render(Context({'obj': self.sponsor}))
        self.assertEqual(rendered, '')

    def test_renders_none(self):
        template = Template("{% load bilingual %}{% bilingual obj 'url' %}")
        sponsor = SponsorFactory(url_en=None)
        rendered = template.render(Context({'obj': sponsor}))
        self.assertEqual(rendered, '')

    def test_renders_attribute(self):
        template = Template("{% load bilingual %}{% bilingual obj 'logo' 'url' %}")
        rendered = template.render(Context({'obj': self.sponsor}))
        self.assertIn('/media/sponsor_files/example_', rendered)

    def test_renders_attribute_value_error(self):
        sponsor = SponsorFactory(logo_en=None)
        template = Template("{% load bilingual %}{% bilingual obj 'logo' 'url' %}")
        rendered = template.render(Context({'obj': sponsor}))
        self.assertEqual(rendered, '')
