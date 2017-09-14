from django.core.management.base import BaseCommand
from pyconca2017.pycon_schedule.services import PresentationService
from pyconca2017.pycon_schedule.models import Presentation, Speaker


class Command(BaseCommand):
    help = 'Sync approved Papercall proposals with the database'

    def add_arguments(self, parser):
        parser.add_argument('--update', action='store_true', dest='update')

    def handle(self, *args, **options):
        presentations_count = Presentation.objects.count()
        speaker_count = Speaker.objects.count()

        service = PresentationService()
        service.sync_proposals(update=options['update'])

        presentations_count_after = Presentation.objects.count()
        speaker_count_after = Speaker.objects.count()

        presentations_created = presentations_count_after - presentations_count
        speakers_created = speaker_count_after - speaker_count

        self.stdout.write('Success!')
        self.stdout.write('Presentations created: {}'.format(presentations_created))
        self.stdout.write('Speakers created: {}'.format(speakers_created))
