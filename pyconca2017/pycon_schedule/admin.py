from django.contrib.admin import ModelAdmin, register
from pyconca2017.pycon_schedule.models import Speaker, Presentation


@register(Speaker)
class SpeakerAdmin(ModelAdmin):
    pass


@register(Presentation)
class PresentationAdmin(ModelAdmin):
    pass
