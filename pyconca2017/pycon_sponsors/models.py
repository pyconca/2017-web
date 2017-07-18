from django.db import models
from django.utils.translation import ugettext_lazy as _


class PySponsorLevel(models.Model):
    name_en = models.CharField(max_length=255)
    name_fr = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    description_en = models.TextField(default='', blank=True)
    description_fr = models.TextField(default='', blank=True)

    def __str__(self):
        return self.name_en

    def sponsors(self):
        return self.py_sponsors.filter(active=True).order_by('order')

    def has_sponsors(self):
        return self.sponsors().count()


class PySponsor(models.Model):

    title_en = models.CharField(max_length=255, blank=True, default='')
    title_fr = models.CharField(max_length=255, blank=True, default='')
    description_en = models.TextField(blank=True, default='')
    description_fr = models.TextField(blank=True, default='')
    twitter_username_en = models.CharField(max_length=255, blank=True, default='')
    twitter_username_fr = models.CharField(max_length=255, blank=True, default='')
    url_en = models.URLField(blank=True, null=True)
    url_fr = models.URLField(blank=True, null=True)
    logo_en = models.FileField(_("Logo EN"), blank=True, upload_to="sponsor_files")
    logo_fr = models.FileField(_("Logo FR"), blank=True, upload_to="sponsor_files")

    active = models.BooleanField(default=False)
    internal_note = models.TextField(_('Internal note'), default='', blank=True)
    added_on = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    level = models.ForeignKey(PySponsorLevel, related_name='py_sponsors')

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.title_en

    @property
    def twitter_url_en(self):
        if self.twitter_username_en is None:
            return None
        return 'https://twitter.com/%s' % self.twitter_username_en

    @property
    def twitter_url_fr(self):
        if self.twitter_username_fr is None:
            return None
        return 'https://twitter.com/%s' % self.twitter_username_fr
