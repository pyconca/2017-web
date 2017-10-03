from datetime import time, date

from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from pyconca2017.pycon_schedule.models import Schedule, ScheduleSlot, SlotEvent, Location


SCHEDULE_SLOTS = {
    date(2017, 11, 18): [
        {'start': time(8), 'end': time(9), 'content': 'Registration & Breakfast'},

        # Morning keynote
        {'start': time(9), 'end': time(10, 30), 'content': 'Welcome & Morning Keynote'},

        # 3 x 30 min
        {'start': time(10, 30), 'end': time(11, 00), 'track': Location.Tracks.TRACK_ONE, 'ref': 'Sat/A/30/1'},
        {'start': time(10, 30), 'end': time(11, 00), 'track': Location.Tracks.TRACK_TWO, 'ref': 'Sat/A/30/1'},
        {'start': time(10, 30), 'end': time(11, 00), 'track': Location.Tracks.TRACK_THREE, 'ref': 'Sat/A/30/1'},
        {'start': time(11, 10), 'end': time(11, 40), 'track': Location.Tracks.TRACK_ONE, 'ref': 'Sat/A/30/2'},
        {'start': time(11, 10), 'end': time(11, 40), 'track': Location.Tracks.TRACK_TWO, 'ref': 'Sat/A/30/2'},
        {'start': time(11, 10), 'end': time(11, 40), 'track': Location.Tracks.TRACK_THREE, 'ref': 'Sat/A/30/2'},
        {'start': time(11, 50), 'end': time(12, 20), 'track': Location.Tracks.TRACK_ONE, 'ref': 'Sat/A/30/3'},
        {'start': time(11, 50), 'end': time(12, 20), 'track': Location.Tracks.TRACK_TWO, 'ref': 'Sat/A/30/3'},
        {'start': time(11, 50), 'end': time(12, 20), 'track': Location.Tracks.TRACK_THREE, 'ref': 'Sat/A/30/3'},
        # Tutorial 1
        {'start': time(11, 10), 'end': time(12, 20), 'track': Location.Tracks.TRACK_TUTORIAL, 'ref': 'Sat/A/30/2'},

        # Lunch
        {'start': time(12, 20), 'end': time(13, 35), 'content': 'Lunch'},

        # 3 x 10 min
        {'start': time(13, 35), 'end': time(13, 45), 'track': Location.Tracks.TRACK_ONE, 'ref': 'Sat/B/10/1'},
        {'start': time(13, 35), 'end': time(13, 45), 'track': Location.Tracks.TRACK_TWO, 'ref': 'Sat/B/10/1'},
        {'start': time(13, 35), 'end': time(13, 45), 'track': Location.Tracks.TRACK_THREE, 'ref': 'Sat/B/10/1'},
        {'start': time(13, 50), 'end': time(14, 00), 'track': Location.Tracks.TRACK_ONE, 'ref': 'Sat/B/10/2'},
        {'start': time(13, 50), 'end': time(14, 00), 'track': Location.Tracks.TRACK_TWO, 'ref': 'Sat/B/10/2'},
        {'start': time(13, 50), 'end': time(14, 00), 'track': Location.Tracks.TRACK_THREE, 'ref': 'Sat/B/10/2'},
        {'start': time(14, 5), 'end': time(14, 15), 'track': Location.Tracks.TRACK_ONE, 'ref': 'Sat/B/10/3'},
        {'start': time(14, 5), 'end': time(14, 15), 'track': Location.Tracks.TRACK_TWO, 'ref': 'Sat/B/10/3'},
        {'start': time(14, 5), 'end': time(14, 15), 'track': Location.Tracks.TRACK_THREE, 'ref': 'Sat/B/10/3'},
        # Tutorial 2
        {'start': time(13, 35), 'end': time(14, 15), 'track': Location.Tracks.TRACK_TUTORIAL, 'ref': 'Sat/B/10/1'},

        # 2 x 30 min
        {'start': time(14, 20), 'end': time(14, 50), 'track': Location.Tracks.TRACK_ONE, 'ref': 'Sat/C/30/1'},
        {'start': time(14, 20), 'end': time(14, 50), 'track': Location.Tracks.TRACK_TWO, 'ref': 'Sat/C/30/1'},
        {'start': time(14, 20), 'end': time(14, 50), 'track': Location.Tracks.TRACK_THREE, 'ref': 'Sat/C/30/1'},
        {'start': time(15), 'end': time(15, 30), 'track': Location.Tracks.TRACK_ONE, 'ref': 'Sat/C/30/2'},
        {'start': time(15), 'end': time(15, 30), 'track': Location.Tracks.TRACK_TWO, 'ref': 'Sat/C/30/2'},
        {'start': time(15), 'end': time(15, 30), 'track': Location.Tracks.TRACK_THREE, 'ref': 'Sat/C/30/2'},
        # Tutorial 3
        {'start': time(14, 20), 'end': time(15, 20), 'track': Location.Tracks.TRACK_TUTORIAL, 'ref': 'Sat/C/30/1'},

        # Break
        {'start': time(15, 30), 'end': time(16), 'content': 'Break'},

        # 2 x 30 min
        {'start': time(16), 'end': time(16, 30), 'track': Location.Tracks.TRACK_ONE, 'ref': 'Sat/D/30/1'},
        {'start': time(16), 'end': time(16, 30), 'track': Location.Tracks.TRACK_TWO, 'ref': 'Sat/D/30/1'},
        {'start': time(16), 'end': time(16, 30), 'track': Location.Tracks.TRACK_THREE, 'ref': 'Sat/D/30/1'},
        {'start': time(16, 40), 'end': time(17, 10), 'track': Location.Tracks.TRACK_ONE, 'ref': 'Sat/D/30/2'},
        {'start': time(16, 40), 'end': time(17, 10), 'track': Location.Tracks.TRACK_TWO, 'ref': 'Sat/D/30/2'},
        {'start': time(16, 40), 'end': time(17, 10), 'track': Location.Tracks.TRACK_THREE, 'ref': 'Sat/D/30/2'},

        # Afternoon keynote
        {'start': time(17, 30), 'end': time(18, 30), 'content': 'Afternoon Keynote'},
    ],
    date(2017, 11, 19): [
        {'start': time(9), 'end': time(10), 'content': 'Breakfast'},

        # Morning keynote
        {'start': time(10), 'end': time(11, 00), 'content': 'Welcome & Morning Keynote'},

        # 3 x 30 min
        {'start': time(11, 10), 'end': time(11, 40), 'track': Location.Tracks.TRACK_ONE, 'ref': 'Sun/A/30/1'},
        {'start': time(11, 10), 'end': time(11, 40), 'track': Location.Tracks.TRACK_TWO, 'ref': 'Sun/A/30/1'},
        {'start': time(11, 10), 'end': time(11, 40), 'track': Location.Tracks.TRACK_THREE, 'ref': 'Sun/A/30/1'},
        {'start': time(11, 50), 'end': time(12, 10), 'track': Location.Tracks.TRACK_ONE, 'ref': 'Sun/A/30/2'},
        {'start': time(11, 50), 'end': time(12, 10), 'track': Location.Tracks.TRACK_TWO, 'ref': 'Sun/A/30/2'},
        {'start': time(11, 50), 'end': time(12, 10), 'track': Location.Tracks.TRACK_THREE, 'ref': 'Sun/A/30/2'},
        {'start': time(12, 30), 'end': time(13, 00), 'track': Location.Tracks.TRACK_ONE, 'ref': 'Sun/A/30/3'},
        {'start': time(12, 30), 'end': time(13, 00), 'track': Location.Tracks.TRACK_TWO, 'ref': 'Sun/A/30/3'},
        {'start': time(12, 30), 'end': time(13, 00), 'track': Location.Tracks.TRACK_THREE, 'ref': 'Sun/A/30/3'},
        # Tutorial 1
        {'start': time(11, 50), 'end': time(13, 00), 'track': Location.Tracks.TRACK_TUTORIAL, 'ref': 'Sun/A/30/1'},

        # Lunch
        {'start': time(13, 00), 'end': time(13, 55), 'content': 'Lunch'},

        # 3 x 10 min
        {'start': time(13, 55), 'end': time(14, 5), 'track': Location.Tracks.TRACK_ONE, 'ref': 'Sun/B/10/1'},
        {'start': time(13, 55), 'end': time(14, 5), 'track': Location.Tracks.TRACK_TWO, 'ref': 'Sun/B/10/1'},
        {'start': time(13, 55), 'end': time(14, 5), 'track': Location.Tracks.TRACK_THREE, 'ref': 'Sun/B/10/1'},
        {'start': time(14, 10), 'end': time(14, 20), 'track': Location.Tracks.TRACK_ONE, 'ref': 'Sun/B/10/2'},
        {'start': time(14, 10), 'end': time(14, 20), 'track': Location.Tracks.TRACK_TWO, 'ref': 'Sun/B/10/2'},
        {'start': time(14, 10), 'end': time(14, 20), 'track': Location.Tracks.TRACK_THREE, 'ref': 'Sun/B/10/2'},
        {'start': time(14, 25), 'end': time(14, 35), 'track': Location.Tracks.TRACK_ONE, 'ref': 'Sun/B/10/3'},
        {'start': time(14, 25), 'end': time(14, 35), 'track': Location.Tracks.TRACK_TWO, 'ref': 'Sun/B/10/3'},
        {'start': time(14, 25), 'end': time(14, 35), 'track': Location.Tracks.TRACK_THREE, 'ref': 'Sun/B/10/3'},
        # Tutorial 2
        {'start': time(13, 55), 'end': time(14, 35), 'track': Location.Tracks.TRACK_TUTORIAL, 'ref': 'Sun/B/10/1'},

        # 1 x 30 min
        {'start': time(14, 45), 'end': time(15, 15), 'track': Location.Tracks.TRACK_ONE, 'ref': 'Sun/C/30/1'},
        {'start': time(14, 45), 'end': time(15, 15), 'track': Location.Tracks.TRACK_TWO, 'ref': 'Sun/C/30/1'},
        {'start': time(14, 45), 'end': time(15, 15), 'track': Location.Tracks.TRACK_THREE, 'ref': 'Sun/C/30/1'},

        # Break
        {'start': time(15, 15), 'end': time(15, 40), 'content': 'Break'},

        # 2 x 30 min
        {'start': time(15, 40), 'end': time(16, 10), 'track': Location.Tracks.TRACK_ONE, 'ref': 'Sun/D/30/1'},
        {'start': time(15, 40), 'end': time(16, 10), 'track': Location.Tracks.TRACK_TWO, 'ref': 'Sun/D/30/1'},
        {'start': time(15, 40), 'end': time(16, 10), 'track': Location.Tracks.TRACK_THREE, 'ref': 'Sun/D/30/1'},
        {'start': time(16, 20), 'end': time(16, 50), 'track': Location.Tracks.TRACK_ONE, 'ref': 'Sun/D/30/2'},
        {'start': time(16, 20), 'end': time(16, 50), 'track': Location.Tracks.TRACK_TWO, 'ref': 'Sun/D/30/2'},
        {'start': time(16, 20), 'end': time(16, 50), 'track': Location.Tracks.TRACK_THREE, 'ref': 'Sun/D/30/2'},
        # Tutorial 3
        {'start': time(15, 40), 'end': time(16, 50), 'track': Location.Tracks.TRACK_TUTORIAL, 'ref': 'Sun/D/30/1'},

        # Afternoon keynote
        {'start': time(17), 'end': time(18), 'content': 'Afternoon Keynote & Closing Message'},
    ]
}


class Command(BaseCommand):
    help = 'Init schedule slots'

    def handle(self, *args, **options):

        with transaction.atomic():
            for _date, slots in SCHEDULE_SLOTS.items():
                if Schedule.objects.filter(day=_date).exists():
                    raise CommandError('Schedule for {} already exists'.format(_date))
                schedule = Schedule.objects.create(day=_date)
                for slot in slots:
                    slot_obj = ScheduleSlot.objects.get_or_create(
                        schedule=schedule,
                        start_time=slot['start'],
                        end_time=slot['end'],
                        ref=slot.get('ref')
                    )[0]
                    content = slot.get('content')
                    track = slot.get('track')
                    if track or content:
                        location = Location.objects.get_or_create(
                            track=track,
                            defaults={'name': dict(Location.Tracks.choices)[track]}
                        )[0] if track else None
                        SlotEvent.objects.create(
                            slot=slot_obj,
                            content=content or '',
                            location=location
                        )

        self.stdout.write('Done!')
