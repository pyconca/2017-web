from django.contrib.admin import ModelAdmin, register
from pyconca2017.pycon_schedule.models import (
    Speaker,
    Presentation,
    Schedule,
    ScheduleSlot,
    Location,
    SlotEvent,
)


@register(Speaker)
class SpeakerAdmin(ModelAdmin):
    pass


@register(Presentation)
class PresentationAdmin(ModelAdmin):
    list_display = ('__str__', 'speaker', 'audience_level', 'presentation_format', 'papercall_id')


@register(Schedule)
class ScheduleAdmin(ModelAdmin):
    pass


@register(ScheduleSlot)
class ScheduleSlotAdmin(ModelAdmin):
    list_display = ('__str__', 'ref', 'schedule', 'start_time', 'end_time', 'duration')


@register(Location)
class LocationAdmin(ModelAdmin):
    list_display = ('name', 'track', 'order', 'capacity')


@register(SlotEvent)
class SlotEventAdmin(ModelAdmin):
    list_display = ('__str__', 'location', 'slot', 'presentation', 'presenter')
    ordering = ('slot__schedule__day', 'slot__start_time', 'slot__end_time', 'location')
