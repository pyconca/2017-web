from django.db import models
from django.utils.text import ugettext_lazy as _

from symposion.proposals.models import ProposalBase


class Proposal(ProposalBase):

    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    AUDIENCE_LEVEL_INTERMEDIATE = 3

    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, "Novice"),
        (AUDIENCE_LEVEL_INTERMEDIATE, "Intermediate"),
        (AUDIENCE_LEVEL_EXPERIENCED, "Experienced"),
    ]

    audience_level = models.IntegerField(choices=AUDIENCE_LEVELS)

    recording_release = models.BooleanField(
        default=True,
        help_text="By submitting your proposal, you agree to give permission to the conference organizers to record,"
                  " edit, and release audio and/or video of your presentation. If you do not agree to this, "
                  "please uncheck this box."
    )

    YES = 1
    NO = 0
    YES_NO_CHOICES = ((YES, 'Yes'), (NO, 'No'))

    recurring = models.PositiveSmallIntegerField(choices=YES_NO_CHOICES,
                                                 default=0,
                                                 help_text=_("Have you given this talk before?"),
                                                 verbose_name=_("Previously given"))
    tutorial = models.PositiveSmallIntegerField(choices=YES_NO_CHOICES,
                                                default=0,
                                                help_text=_("Would you be interested in receiving mentorship /"
                                                            " input on your talk in advance?"),
                                                verbose_name=_("Speaker mentorship"))

    DURATION_SHORT = 'short'
    DURATION_MEDIUM = 'medium'
    DURATION_LONG = 'long'
    DURATION_CHOICES = (
        (DURATION_SHORT, 'Short (~10 minutes)'),
        (DURATION_MEDIUM, 'Long (~30 minutes)'),
        (DURATION_LONG, 'Classroom tutorial (~45-60 minutes)'),
    )

    duration = models.CharField(choices=DURATION_CHOICES,
                                max_length=16,
                                default=DURATION_MEDIUM,
                                verbose_name=_("Duration"))

    class Meta:
        abstract = True

    @property
    def duration_display(self):
        return dict(self.DURATION_CHOICES).get(self.duration)

    @property
    def tutorial_display(self):
        return 'Yes' if self.tutorial else 'No'

    @property
    def recurring_display(self):
        return 'Yes' if self.recurring else 'No'


class TalkProposal(Proposal):

    class Meta:
        verbose_name = "talk proposal"
        permissions = (
            ('can_review_unbiased', 'Can review with speaker details'),
        )


class TutorialProposal(Proposal):
    class Meta:
        verbose_name = "tutorial proposal"
