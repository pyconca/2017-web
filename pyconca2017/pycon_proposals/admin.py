from django.contrib import admin

from .models import TalkProposal, TutorialProposal


@admin.register(TalkProposal, TutorialProposal)
class TalkProposalAdmin(admin.ModelAdmin):

    list_display = ('title', 'kind', 'tutorial', 'audience_level', 'speaker')
    list_filter = ('kind', 'recurring', 'tutorial', 'audience_level', 'speaker', 'duration')
    search_fields = ('title', 'description', 'abstract')
