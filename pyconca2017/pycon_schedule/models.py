from datetime import datetime

import bleach
import markdown
from django.db import models


""" Presentation """


class Speaker(models.Model):
    """ Who """
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    bio = models.TextField(default='')
    twitter_username = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(max_length=2048, null=True, blank=True)
    shirt_size = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    is_keynote = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

    @property
    def twitter_url(self):
        if not self.twitter_username:
            return None

        return 'https://twitter.com/{}'.format(self.twitter_username)

    def bio_html(self):
        return markdown.markdown(bleach.clean(self.bio), extensions=["extra"], safe_mode=False)


class Presentation(models.Model):
    """ What """
    papercall_id = models.IntegerField(null=True, blank=True, unique=True)

    title = models.CharField(max_length=255)
    description = models.TextField(default='')
    notes = models.TextField(default='')
    abstract = models.TextField(default='')
    audience_level = models.CharField(max_length=255)
    presentation_format = models.CharField(max_length=255)

    speaker = models.ForeignKey(Speaker)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)

    def description_html(self):
        return markdown.markdown(bleach.clean(self.description), extensions=["extra"], safe_mode=False)


""" Schedule """


class Schedule(models.Model):
    """ When (what day) """
    day = models.DateField(unique=True)

    def __str__(self):
        return self.day.strftime('%b %d')


class Location(models.Model):
    """ Where """
    class Tracks(object):
        TRACK_ONE = 'track-1'
        TRACK_TWO = 'track-2'
        TRACK_THREE = 'track-3'
        TRACK_TUTORIAL = 'tutorial'

        choices = (
            (TRACK_ONE, 'Track 1'),
            (TRACK_TWO, 'Track 2'),
            (TRACK_THREE, 'Track 3'),
            (TRACK_TUTORIAL, 'Tutorial'),
        )

    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    capacity = models.PositiveIntegerField(default=0)
    notes = models.TextField(default='', blank=True)
    track = models.CharField(max_length=255, choices=Tracks.choices, null=True, blank=True)

    def __str__(self):
        return self.name


class ScheduleSlot(models.Model):
    """ When (what time) """
    schedule = models.ForeignKey(Schedule, related_name='slots')
    start_time = models.TimeField()
    end_time = models.TimeField()

    ref = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return '{} - {} ({})'.format(self.start_time, self.end_time, self.schedule)

    class Meta:
        unique_together = (('schedule', 'start_time', 'end_time'),)
        ordering = ('schedule', 'start_time', 'end_time')

    @property
    def duration(self):
        return datetime.combine(self.schedule.day, self.end_time) - datetime.combine(self.schedule.day, self.start_time)

    @property
    def start_events(self):
        return SlotEvent.objects.select_related('location').filter(slot__schedule=self.schedule,
                                                                   slot__start_time=self.start_time).order_by(
            'location__order')


class SlotEvent(models.Model):
    """ Glue what with when and where """
    slot = models.ForeignKey(ScheduleSlot, related_name='events')
    location = models.ForeignKey(Location, null=True, blank=True)
    content = models.TextField('Content (EN)', blank=True)
    content_fr = models.TextField('Content (FR)', blank=True)

    presentation = models.OneToOneField(Presentation, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = (
            ('slot', 'location'),
        )
        ordering = ('location__order',)

    @property
    def title(self):
        if self.presentation:
            return self.presentation.title

        return self.content

    @property
    def is_presentation(self):
        return bool(self.presentation)

    @property
    def duration(self):
        return self.slot.duration

    @property
    def duration_str(self):
        return ':'.join(str(self.duration).split(':')[:2])

    @property
    def presenter(self):
        if self.presentation:
            return self.presentation.speaker
