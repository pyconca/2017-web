import json

import requests

from django.conf import settings

from pyconca2017.pycon_schedule.models import Speaker, Presentation


class PapercallInterface(object):

    BASE_URL = 'https://www.papercall.io/api/v1'

    EVENT_URL = '/event'
    SUBMISSIONS_LIST_URL = '/submissions'
    SUBMISSION_GET_URL = '/submissions/{submission_id}'
    SUBMISSION_RATINGS_URL = '/submissions/{submission_id}/ratings'

    class SubmissionStates(object):
        ACCEPTED = 'accepted'
        SUBMITTED = 'submitted'
        REJECTED = 'rejected'
        WAITLIST = 'waitlist'

    def __init__(self):
        self.client = requests.Session()
        self.client.headers.update({'Authorization': settings.PAPERCALL_TOKEN})

    def get_submissions(self, state=SubmissionStates.ACCEPTED):
        """ Iterator """
        url = '{}{}'.format(self.BASE_URL, self.SUBMISSIONS_LIST_URL)
        params = {
            'per_page': 100,
            'page': 0,
            'order': 'created_at',
        }
        if state:
            params['state'] = state

        while True:
            params['page'] += 1
            response = self.client.get(url, params=params)

            response_pagination = json.loads(response.headers.get('x-pagination'))

            data = response.json()

            for item in data:
                yield item

            if response_pagination['last_page']:
                break


class PresentationService(object):

    def __init__(self):
        self.papercall = PapercallInterface()

    def sync_proposals(self, update=False):
        """
        Sync Papercall submissions with the database.

        :param update: If True, all values will be updated from Papercall.
        :return:
        """

        for submission in self.papercall.get_submissions():
            speaker_data = self._submission_to_speaker_data(submission)
            talk_data = self._submission_to_presentation_data(submission)

            speaker = self._sync_speaker(speaker_data, update=update)
            talk_data['speaker'] = speaker
            self._sync_presentation(talk_data, update=update)

    def _submission_to_speaker_data(self, submission):
        profile = submission['profile']
        return {
            'full_name': profile['name'],
            'bio': profile['bio'],
            'twitter_username': profile['twitter'],
            'company_name': profile['company'],
            'url': profile['url'],
            'shirt_size': profile['shirt_size'],
            'email': profile['email'],
            'location': profile['location'],
        }

    def _sync_speaker(self, speaker_data, update=False):
        if update:
            speaker = Speaker.objects.update_or_create(email=speaker_data['email'], defaults=speaker_data)[0]
        else:
            speaker = Speaker.objects.get_or_create(email=speaker_data.pop('email'), defaults=speaker_data)[0]

        return speaker

    def _submission_to_presentation_data(self, submission):
        talk = submission['talk']

        return {
            'papercall_id': submission['id'],
            'title': talk['title'],
            'description': talk['description'],
            'notes': talk['notes'],
            'abstract': talk['abstract'],
            'audience_level': talk['audience_level'],
            'presentation_format': talk['talk_format'],
        }

    def _sync_presentation(self, data, update=False):
        if update:
            presentation = Presentation.objects.update_or_create(papercall_id=data['papercall_id'], defaults=data)[0]
        else:
            presentation = Presentation.objects.get_or_create(papercall_id=data.pop('papercall_id'), defaults=data)[0]

        return presentation
