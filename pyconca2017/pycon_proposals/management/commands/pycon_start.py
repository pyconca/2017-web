from datetime import date, datetime
import pytz

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone

from symposion.conference.models import Conference, Section
from symposion.proposals.models import ProposalKind, ProposalSection

from pyconca2017.pycon_proposals.models import TalkProposal, TutorialProposal

data = {
    'title': 'PyCon Canada 2017',
    'start_date': date(2017, 11, 10),
    'end_date': date(2017, 11, 12),

    'sections': [{
        'slug': 'talks',
        'name': 'Talks',
        'start_date': date(2017, 11, 11),
        'end_date': date(2017, 11, 12),
    }, {
        'slug': 'tutorials',
        'name': 'Tutorials',
        'start_date': date(2017, 11, 11),
        'end_date': date(2017, 11, 12),
    }],

    'proposal_kinds': [{
        'section': 'talks',
        'name': 'Task',
        'slug': 'talk'
    }, {
        'section': 'tutorials',
        'name': 'Tutorial',
        'slug': 'tutorial'
    }],

    'proposal_sections': [{
        'section': 'talks',
        'start': datetime(2017, 4, 1, tzinfo=pytz.timezone(settings.TIME_ZONE)),
        'end': datetime(2017, 6, 30, 23, 59, 59, tzinfo=pytz.timezone(settings.TIME_ZONE)),
        'published': True,
        'closed': False,
    }, {
        'section': 'tutorials',
        'start': datetime(2017, 4, 1, tzinfo=pytz.timezone(settings.TIME_ZONE)),
        'end': datetime(2017, 6, 30, 23, 59, 59, tzinfo=pytz.timezone(settings.TIME_ZONE)),
        'published': True,
        'closed': False,
    }]
}


class Command(BaseCommand):
    help = 'Setup PyCon CA 2017'
    jobs = [
        'setup_conference',
        'setup_sections',
        'setup_proposals',
    ]

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):

        for n, job in enumerate(self.jobs):
            method_handler = getattr(self, job)
            self.stdout.write(self.style.NOTICE('({}/{}) >>> {}'.format(n + 1, len(self.jobs), method_handler.__doc__)))
            method_handler()

        self.stdout.write(self.style.SUCCESS('{title} is ready!'.format(**data)))

    def setup_conference(self):
        """ Create conference if does not exist. """
        conf_id = settings.CONFERENCE_ID

        conf_data = {
            'title': data['title'],
            'start_date': data['start_date'],
            'end_date': data['end_date'],
        }

        try:
            conference = Conference.objects.get(id=conf_id)
            for field, value in conf_data.items():
                setattr(conference, field, value)
            conference.save()
        except Conference.DoesNotExist:
            Conference.objects.create(id=conf_id, **conf_data)

        self.stdout.write('Done!')

    def setup_sections(self):
        """ Create conference sections. """
        for section_data in data['sections']:
            section, _created = Section.objects.get_or_create(slug=section_data['slug'],
                                                              conference_id=settings.CONFERENCE_ID,
                                                              defaults=section_data)
            if not _created:
                for field, value in section_data.items():
                    setattr(section, field, value)
                section.save()

        self.stdout.write('Done!')

    def setup_proposals(self):

        for _kind in data['proposal_kinds']:
            _kind['section'] = Section.objects.get(slug=_kind['section'])
            try:
                kind = ProposalKind.objects.get(slug=_kind['slug'], section=_kind['section'])
                for field, value in _kind.items():
                    setattr(kind, field, value)
                kind.save()
            except ProposalKind.DoesNotExist:
                ProposalKind.objects.create(**_kind)

        for _section in data['proposal_sections']:
            _section['section'] = Section.objects.get(slug=_section['section'])
            try:
                section = ProposalSection.objects.get(section=_section['section'])
                for field, value in _section.items():
                    setattr(section, field, value)
                section.save()
            except ProposalSection.DoesNotExist:
                ProposalSection.objects.create(**_section)

        self.stdout.write('Done!')
