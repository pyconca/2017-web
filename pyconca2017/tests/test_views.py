from test_plus.test import TestCase


class WebPagesTests(TestCase):

    def test_homepage(self):
        response = self.client.get(self.reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get(self.reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_venue(self):
        response = self.client.get(self.reverse('venue'))
        self.assertEqual(response.status_code, 200)

    def test_sponsors(self):
        response = self.client.get(self.reverse('sponsors:sponsors'))
        self.assertEqual(response.status_code, 200)

    def test_code_of_conduct(self):
        response = self.client.get(self.reverse('code-of-conduct'))
        self.assertEqual(response.status_code, 200)

    def test_volunteer(self):
        response = self.client.get(self.reverse('volunteer'))
        self.assertEqual(response.status_code, 200)

    def test_schedule(self):
        response = self.client.get(self.reverse('schedule'))
        self.assertEqual(response.status_code, 200)
