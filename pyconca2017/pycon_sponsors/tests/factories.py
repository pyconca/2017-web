import factory

from pyconca2017.pycon_sponsors.models import PySponsor, PySponsorLevel


class LevelFactory(factory.DjangoModelFactory):

    class Meta:
        model = PySponsorLevel

    name_en = 'Gold'
    name_fr = 'Or'


class SponsorFactory(factory.DjangoModelFactory):

    class Meta:
        model = PySponsor

    name_en = 'Demo EN'
    name_fr = 'Demo FR'
    description_en = 'English text'
    description_fr = 'Français'
    twitter_username_en = 'demo_en'
    twitter_username_fr = 'demo_fr'
    url_en = 'http://www.pycon.ca/en'
    url_fr = 'http://www.pycon.ca/fr'
    logo_en = factory.django.FileField()
    logo_fr = factory.django.FileField()

    active = True
    level = factory.SubFactory(LevelFactory)
