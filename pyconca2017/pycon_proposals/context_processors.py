from symposion.conference.models import current_conference

organizers = (
    ('Terry Yanchynskyy', 'https://github.com/onebit0fme'),
    ('Myles Braithwaite', 'https://mylesb.ca/'),
    ('Francis Deslauriers', 'https://twitter.com/francisDeslaur'),
    ('Peter McCormick', 'https://twitter.com/pdmccormick'),
)

organizers = sorted(organizers, key=lambda x: x[0])


def conference_context(request):

    return {
        "CONFERENCE": current_conference(),
        "ORGANIZERS": organizers,
    }
