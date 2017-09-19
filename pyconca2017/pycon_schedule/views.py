from datetime import date

from django.http import Http404
from django.views.generic import TemplateView, RedirectView
from django.urls import NoReverseMatch, reverse

from pyconca2017.pycon_schedule.models import Schedule, Location


class ScheduleView(TemplateView):
    template_name = 'schedule/schedule.html'

    def get_queryset(self):
        return Schedule.objects.prefetch_related(
            'slots',
            'slots__events',
            'slots__events__location',
            'slots__events__presentation',
        )

    def get_context_data(self, **kwargs):
        print(kwargs)
        schedule_date = kwargs.get('schedule_date')
        schedule = self.get_queryset().filter(day=schedule_date)
        if not schedule_date or not schedule.exists():
            raise Http404()

        context = super().get_context_data(**kwargs)
        context['schedules_all'] = Schedule.objects.order_by('day')
        context['schedule'] = schedule.get()
        context['locations'] = Location.objects.all() # TODO: only show locations for given day.

        return context


class ScheduleRedirectView(RedirectView):
    permanent = True
    pattern_name = 'schedule:detail'

    def get_redirect_url(self, *args, **kwargs):
        """ Redirect to the most appropriate schedule. """
        if not Schedule.objects.exists():
            raise Http404

        try:
            schedule_day = Schedule.objects.filter(day__gte=date.today()).order_by('day').first().day.strftime('%Y-%m-%d')
        except Schedule.DoesNotExist:
            schedule_day = Schedule.objects.order_by('day').first().day.strftime('%Y-%m-%d')

        try:
            url = reverse(self.pattern_name, kwargs={'schedule_date': schedule_day})
        except NoReverseMatch:
            raise Http404

        return url
