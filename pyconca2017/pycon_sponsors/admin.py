from django.contrib import admin

from pyconca2017.pycon_sponsors.models import PySponsorLevel, PySponsor


@admin.register(PySponsorLevel)
class SponsorLevelAdmin(admin.ModelAdmin):
    pass


@admin.register(PySponsor)
class SponsorAdmin(admin.ModelAdmin):
    pass
