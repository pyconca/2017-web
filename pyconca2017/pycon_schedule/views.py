from django.views.generic import TemplateView

from pyconca2017.pycon_schedule.models import Schedule


class SchedulePreview(TemplateView):
    template_name = 'schedule/schedule_preview.html'

    def get_context_data(self, **kwargs):
        # TODO: schedule date in url
        context = super().get_context_data(**kwargs)

        context['schedule'] = Schedule.objects.prefetch_related(
            'slots',
            'slots__events',
            'slots__events__location',
            'slots__events__presentation',
        ).first()

        return context
