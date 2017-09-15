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
    pass


@register(Schedule)
class ScheduleAdmin(ModelAdmin):
    pass


@register(ScheduleSlot)
class ScheduleSlotAdmin(ModelAdmin):
    list_display = ('__str__', 'schedule', 'start_time', 'end_time', 'duration')


@register(Location)
class LocationAdmin(ModelAdmin):
    list_display = ('name', 'order', 'capacity')


@register(SlotEvent)
class SlotEventAdmin(ModelAdmin):
    list_display = ('__str__', 'location', 'slot', 'presentation', 'presenter')
    ordering = ('slot__schedule', 'slot__start_time', 'slot__end_time')
