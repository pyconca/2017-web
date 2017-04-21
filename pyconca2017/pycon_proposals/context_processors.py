from symposion.conference.models import current_conference


def conference_context(request):
    return {
        "CONFERENCE": current_conference(),
    }
