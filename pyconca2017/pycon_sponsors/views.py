from django.views.generic import TemplateView

from pyconca2017.pycon_sponsors.services import SponsorsService


class SponsorsPageView(TemplateView):
    template_name = 'pages/sponsors.html'

    service = SponsorsService()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        levels = self.service.get_levels()

        context_data['sponsor_levels'] = levels

        return context_data
