import csv
from io import StringIO

from django import forms

from pyconca2017.pycon_schedule.models import Location, Presentation, SlotEvent


class AssignCSVForm(forms.Form):
    file = forms.FileField()

    def save(self):
        file = self.cleaned_data['file']
        decoded_file = file.read().decode('utf-8')
        io_string = StringIO(decoded_file)
        reader = csv.DictReader(io_string, dialect=csv.excel)
        for row in reader:
            ref = row['Ref']
            for track in ['Track 1', 'Track 2', 'Track 3', 'Tutorial']:
                track_slug = {
                    'Track 1': Location.Tracks.TRACK_ONE,
                    'Track 2': Location.Tracks.TRACK_TWO,
                    'Track 3': Location.Tracks.TRACK_THREE,
                    'Tutorial': Location.Tracks.TRACK_TUTORIAL,
                }[track]
                presentation_id = row[track]
                if presentation_id:
                    try:
                        presentation = Presentation.objects.get(papercall_id=presentation_id)
                    except Presentation.DoesNotExist:
                        # TODO: not synced
                        continue
                    loc = Location.objects.get(track=track_slug)
                    event = SlotEvent.objects.get(location=loc, slot__ref=ref)
                    event.presentation = presentation
                    event.save()
