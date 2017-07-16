from symposion.conference.models import current_conference
from config.organizers import ORGANIZERS

_organizers = sorted(ORGANIZERS, key=lambda x: x[0])


def conference_context(request):

    return {
        "CONFERENCE": current_conference(),
        "ORGANIZERS": _organizers,
    }
