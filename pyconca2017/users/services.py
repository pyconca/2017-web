from symposion.speakers.models import Speaker


class UserService(object):

    def get_or_create_speaker(self, user):
        speaker, _ = Speaker.objects.get_or_create(user=user, defaults={'name': user.name})

        return speaker
