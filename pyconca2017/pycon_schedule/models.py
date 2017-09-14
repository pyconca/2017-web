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


# class Schedule(models.Model):
#     """ When """
#     day = models.DateField()
#
#
# class Room(models.Model):
#     """ Where """
#     name = models.CharField(max_length=255)
#     order = models.PositiveIntegerField(default=0)
#
#     def __str__(self):
#         return self.name
#
#
# class ScheduleSlot(models.Model):
#     room = models.ForeignKey(Room)
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     presentation = models.ForeignKey(Presentation, null=True, blank=True)
#
#     def __str__(self):
#         return '{}: {} - {}'.format(self.room, self.start_time, self.end_time)

