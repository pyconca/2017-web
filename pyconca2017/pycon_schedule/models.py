from datetime import datetime

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


""" Schedule """


class Schedule(models.Model):
    """ When (what day) """
    day = models.DateField(unique=True)

    def __str__(self):
        return self.day.strftime('%b %d')


class Location(models.Model):
    """ Where """
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    capacity = models.PositiveIntegerField(default=0)
    notes = models.TextField(default='', blank=True)

    def __str__(self):
        return self.name


class ScheduleSlot(models.Model):
    """ When (what time) """
    schedule = models.ForeignKey(Schedule, related_name='slots')
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return '{} - {} ({})'.format(self.start_time, self.end_time, self.schedule)

    class Meta:
        unique_together = (('schedule', 'start_time', 'end_time'),)
        ordering = ('schedule', 'start_time', 'end_time')

    @property
    def duration(self):
        return datetime.combine(self.schedule.day, self.end_time) - datetime.combine(self.schedule.day, self.start_time)


class SlotEvent(models.Model):
    """ Glue what with when and where """
    slot = models.ForeignKey(ScheduleSlot, related_name='events')
    location = models.ForeignKey(Location)
    content = models.TextField(blank=True)

    presentation = models.OneToOneField(Presentation, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = (
            ('slot', 'location'),
        )

    @property
    def title(self):
        if self.presentation:
            return self.presentation.title

        return self.content

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
