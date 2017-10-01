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
        {'start': time(10, 30), 'end': time(11, 00), 'room': 'Room One'},
        {'start': time(10, 30), 'end': time(11, 00), 'room': 'Room Two'},
        {'start': time(10, 30), 'end': time(11, 00), 'room': 'Room Three'},
        {'start': time(11, 10), 'end': time(11, 40), 'room': 'Room One'},
        {'start': time(11, 10), 'end': time(11, 40), 'room': 'Room Two'},
        {'start': time(11, 10), 'end': time(11, 40), 'room': 'Room Three'},
        {'start': time(11, 50), 'end': time(12, 20), 'room': 'Room One'},
        {'start': time(11, 50), 'end': time(12, 20), 'room': 'Room Two'},
        {'start': time(11, 50), 'end': time(12, 20), 'room': 'Room Three'},
        # Tutorial 1
        {'start': time(11, 10), 'end': time(12, 20), 'room': 'Tutorial Room'},

        # Lunch
        {'start': time(12, 20), 'end': time(13, 35), 'content': 'Lunch'},

        # 3 x 10 min
        {'start': time(13, 35), 'end': time(13, 45), 'room': 'Room One'},
        {'start': time(13, 35), 'end': time(13, 45), 'room': 'Room Two'},
        {'start': time(13, 35), 'end': time(13, 45), 'room': 'Room Three'},
        {'start': time(13, 50), 'end': time(14, 00), 'room': 'Room One'},
        {'start': time(13, 50), 'end': time(14, 00), 'room': 'Room Two'},
        {'start': time(13, 50), 'end': time(14, 00), 'room': 'Room Three'},
        {'start': time(14, 5), 'end': time(14, 15), 'room': 'Room One'},
        {'start': time(14, 5), 'end': time(14, 15), 'room': 'Room Two'},
        {'start': time(14, 5), 'end': time(14, 15), 'room': 'Room Three'},
        # Tutorial 2
        {'start': time(13, 35), 'end': time(14, 15), 'room': 'Tutorial Room'},

        # 2 x 30 min
        {'start': time(14, 20), 'end': time(14, 50), 'room': 'Room One'},
        {'start': time(14, 20), 'end': time(14, 50), 'room': 'Room Two'},
        {'start': time(14, 20), 'end': time(14, 50), 'room': 'Room Three'},
        {'start': time(15), 'end': time(15, 30), 'room': 'Room One'},
        {'start': time(15), 'end': time(15, 30), 'room': 'Room Two'},
        {'start': time(15), 'end': time(15, 30), 'room': 'Room Three'},

        # Break
        {'start': time(15, 30), 'end': time(16), 'content': 'Break'},

        # 2 x 30 min
        {'start': time(16), 'end': time(16, 30), 'room': 'Room One'},
        {'start': time(16), 'end': time(16, 30), 'room': 'Room Two'},
        {'start': time(16), 'end': time(16, 30), 'room': 'Room Three'},
        {'start': time(16, 40), 'end': time(17, 10), 'room': 'Room One'},
        {'start': time(16, 40), 'end': time(17, 10), 'room': 'Room Two'},
        {'start': time(16, 40), 'end': time(17, 10), 'room': 'Room Three'},
        # Tutorial 3
        {'start': time(16, 00), 'end': time(17, 10), 'room': 'Tutorial Room'},

        # Afternoon keynote
        {'start': time(17, 30), 'end': time(18, 30), 'content': 'Afternoon Keynote'},
    ],
    date(2017, 11, 19): [
        {'start': time(9), 'end': time(10), 'content': 'Breakfast'},

        # Morning keynote
        {'start': time(10), 'end': time(11, 00), 'content': 'Welcome & Morning Keynote'},

        # 3 x 30 min
        {'start': time(11, 10), 'end': time(11, 40), 'room': 'Room One'},
        {'start': time(11, 10), 'end': time(11, 40), 'room': 'Room Two'},
        {'start': time(11, 10), 'end': time(11, 40), 'room': 'Room Three'},
        {'start': time(11, 50), 'end': time(12, 10), 'room': 'Room One'},
        {'start': time(11, 50), 'end': time(12, 10), 'room': 'Room Two'},
        {'start': time(11, 50), 'end': time(12, 10), 'room': 'Room Three'},
        {'start': time(12, 30), 'end': time(13, 00), 'room': 'Room One'},
        {'start': time(12, 30), 'end': time(13, 00), 'room': 'Room Two'},
        {'start': time(12, 30), 'end': time(13, 00), 'room': 'Room Three'},
        # Tutorial 1
        {'start': time(11, 50), 'end': time(13, 00), 'room': 'Tutorial Room'},

        # Lunch
        {'start': time(13, 00), 'end': time(13, 55), 'content': 'Lunch'},

        # 3 x 10 min
        {'start': time(13, 55), 'end': time(14, 5), 'room': 'Room One'},
        {'start': time(13, 55), 'end': time(14, 5), 'room': 'Room Two'},
        {'start': time(13, 55), 'end': time(14, 5), 'room': 'Room Three'},
        {'start': time(14, 10), 'end': time(14, 20), 'room': 'Room One'},
        {'start': time(14, 10), 'end': time(14, 20), 'room': 'Room Two'},
        {'start': time(14, 10), 'end': time(14, 20), 'room': 'Room Three'},
        {'start': time(14, 25), 'end': time(14, 35), 'room': 'Room One'},
        {'start': time(14, 25), 'end': time(14, 35), 'room': 'Room Two'},
        {'start': time(14, 25), 'end': time(14, 35), 'room': 'Room Three'},
        # Tutorial 2
        {'start': time(13, 55), 'end': time(14, 35), 'room': 'Tutorial Room'},

        # 1 x 30 min
        {'start': time(14, 45), 'end': time(15, 15), 'room': 'Room One'},
        {'start': time(14, 45), 'end': time(15, 15), 'room': 'Room Two'},
        {'start': time(14, 45), 'end': time(15, 15), 'room': 'Room Three'},

        # Break
        {'start': time(15, 15), 'end': time(15, 40), 'content': 'Break'},

        # 2 x 30 min
        {'start': time(15, 40), 'end': time(16, 10), 'room': 'Room One'},
        {'start': time(15, 40), 'end': time(16, 10), 'room': 'Room Two'},
        {'start': time(15, 40), 'end': time(16, 10), 'room': 'Room Three'},
        {'start': time(16, 20), 'end': time(16, 50), 'room': 'Room One'},
        {'start': time(16, 20), 'end': time(16, 50), 'room': 'Room Two'},
        {'start': time(16, 20), 'end': time(16, 50), 'room': 'Room Three'},
        # Tutorial 3
        {'start': time(15, 40), 'end': time(16, 50), 'room': 'Tutorial Room'},

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
                        end_time=slot['end']
                    )[0]
                    content = slot.get('content')
                    room = slot.get('room')
                    if room or content:
                        location = Location.objects.create(name=room) if room else None
                        SlotEvent.objects.create(
                            slot=slot_obj,
                            content=content or '',
                            location=location
                        )

        self.stdout.write('Done!')
