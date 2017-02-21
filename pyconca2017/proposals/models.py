from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.text import ugettext_lazy as _

from ..utilsmodels import BaseModel


class Proposal(BaseModel):
    KIND_SHORT = 'short'
    KIND_LONG = 'long'
    KIND_TUTORIAL = 'tutorial'
    KIND_CHOICES = (
        ('short', 'Short Talk (10 minutes)'),
        ('long', 'Long Talk (30 minutes)'),
        ('tutorial', 'Classroom tutorial (60 minutes)')
    )
    kind = models.CharField(choices=KIND_CHOICES, max_length=10,
                            default=KIND_SHORT, verbose_name=_('kind'))

    title = models.CharField(max_length=100, verbose_name=_('title'))

    description = models.TextField(
        _('brief description'), max_length=400,
        help_text=_('If your proposal is accepted this will be made public '
                    'and printed in the program. Should be one paragraph, '
                    'maximum 400 characters.'))
    abstract = models.TextField(
        _('detailed abstract'),
        help_text=_('Detailed outline. Will be made public if your proposal '
                    'is accepted. Edit using '
                    '<a href="http://commonmark.org/help/" '
                    'target="_blank">Markdown</a>.'))
    additional_notes = models.TextField(
        _('additional notes'), blank=True,
        help_text=_("Anything else you'd like the program committee to know "
                    "when making their selection: your past experience, etc. "
                    "This is not made public. Edit using "
                    "<a href='http://commonmark.org/help/' "
                    "target='_blank'>Markdown</a>."))

    date_submitted = models.DateTimeField(default=now, editable=False,
                                          verbose_name=_('date submitted'))
