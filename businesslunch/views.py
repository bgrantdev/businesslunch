from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from businesslunch.forms import OptInForm, DateForm
from django.views.generic import TemplateView
from businesslunch.models import OptIn
from people.models import Person

import calendar
import datetime

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        return {
            'date' : self.date,
            'opted_in' : self.opted_in,
            'opted_out' : self.opted_out,
            'form' : self.opt_in_form,
        }

    @method_decorator(login_required)
    def dispatch(self, request, date=datetime.date.today(),*args, **kwargs):
        self.date = date
        self.opted_in = OptIn.objects.filter(date=date)
        self.opt_in_form = OptInForm(request.POST or None)
        all_people = Person.objects.all()
        self.opted_out = all_people.exclude(id__in=self.opted_in.values_list('attendee', flat=True))
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.opt_in_form.is_valid():
            opt_in = self.opt_in_form.instance
            opt_in.attendee = Person.objects.get(user=request.user)
            opt_in.date = self.date
            opt_in.save()
            return reverse(redirect( 'home', args=[self.date]))
        return self.render_to_response(self.get_context_data())


class CalendarView(TemplateView):
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.date_form,
            'calendar' : self.calendar,
        }

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.calendar = calendar
        self.date_form = DateForm(request.POST or None)
        return super(CalendarView, self).dispatch(request, *args, **kwargs)