from datetime import date

from django.http import Http404
from django.views.generic import TemplateView, RedirectView, FormView
from django.urls import NoReverseMatch, reverse
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from pyconca2017.pycon_schedule.models import Schedule, Location, Presentation
from pyconca2017.pycon_schedule.forms import AssignCSVForm


class ScheduleView(TemplateView):
    template_name = 'schedule/schedule_preview.html'

    def get_queryset(self):
        return Schedule.objects.prefetch_related(
            'slots',
            'slots__events',
            'slots__events__location',
            'slots__events__presentation',
        )

    def get_context_data(self, **kwargs):
        schedule_date = kwargs.get('schedule_date')
        schedule = self.get_queryset().filter(day=schedule_date)
        if not schedule_date or not schedule.exists():
            raise Http404()

        context = super().get_context_data(**kwargs)
        context['schedules_all'] = Schedule.objects.order_by('day')
        context['schedule'] = schedule.get()
        context['locations'] = Location.objects.all()  # TODO: only show locations for given day.

        return context


class ScheduleRedirectView(RedirectView):
    permanent = True
    pattern_name = 'schedule:detail'

    def get_redirect_url(self, *args, **kwargs):
        """ Redirect to the most appropriate schedule. """
        if not Schedule.objects.exists():
            raise Http404

        try:
            schedule_day = Schedule.objects.filter(day__gte=date.today()).order_by('day').first().day.strftime(
                '%Y-%m-%d')
        except (Schedule.DoesNotExist, AttributeError):
            schedule_day = Schedule.objects.order_by('day').first().day.strftime('%Y-%m-%d')

        try:
            url = reverse(self.pattern_name, kwargs={'schedule_date': schedule_day})
        except NoReverseMatch:
            raise Http404

        return url


class PresentationView(TemplateView):
    template_name = 'schedule/presentation.html'

    def get_queryset(self):
        return Presentation.objects.prefetch_related()

    def get_context_data(self, **kwargs):
        presentation_pk = kwargs.get('presentation_pk')
        presentation = self.get_queryset().filter(pk=presentation_pk)

        context = super().get_context_data(**kwargs)
        context['presentation'] = presentation.get()

        return context


@method_decorator(staff_member_required, name='dispatch')
class AssignFromCSVView(FormView):
    form_class = AssignCSVForm
    template_name = 'schedule/admin/form.html'
    success_url = '/schedule'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class SprintsView(TemplateView):
    template_name = 'schedule/sprints.html'

    def get_queryset(self):
        return Schedule.objects.prefetch_related()

    def get_context_data(self, **kwargs):
        return {'schedules_all': self.get_queryset().all()}
