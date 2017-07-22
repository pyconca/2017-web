from symposion.conference.models import current_conference
from config.organizers import ORGANIZERS
from pyconca2017.pycon_sponsors.services import SponsorsService

_organizers = sorted(ORGANIZERS, key=lambda x: x[0])


def conference_context(request):
    sponsors_service = SponsorsService()

    return {
        "CONFERENCE": current_conference(),
        "ORGANIZERS": _organizers,
        "SPONSORS": sponsors_service.get_sponsors()
    }
