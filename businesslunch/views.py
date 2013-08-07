from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from businesslunch.forms import OptInForm, DateForm
from django.views.generic import TemplateView, View
from businesslunch.models import OptIn
from people.models import Person

import datetime

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        return {
            'date' : self.date,
            'opted_in' : self.opted_in,
            'opted_out' : self.opted_out,
            'form' : self.opt_in_form,
            'events': self.events
        }

    @method_decorator(login_required)
    def dispatch(self, request, date=datetime.date.today().strftime('%Y-%m-%d'),*args, **kwargs):
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        self.opted_in = OptIn.objects.filter(date=date)
        self.opt_in_form = OptInForm(request.POST or None)
        all_people = Person.objects.all()
        self.opted_out = all_people.exclude(id__in=self.opted_in.values_list('attendee', flat=True))
        self.events = self.get_events()
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.opt_in_form.is_valid():
            opt_in = self.opt_in_form.instance
            opt_in.attendee = Person.objects.get(user=request.user)
            opt_in.date = self.date
            opt_in.save()
            return redirect(reverse( 'home'))
        return self.render_to_response(self.get_context_data())

    def get_events(self):
        events = []
        dates = []
        for opt_in in OptIn.objects.all():
            date = opt_in.date.strftime('%Y-%m-%d')
            if date not in dates:
                event_dict = {}
                event_dict['title'] = 'Lunch'
                event_dict['start'] = opt_in.date.strftime('%Y-%m-%d')
                events.append(event_dict)
                dates.append(date)
        return events

class JoinView(View):

    @method_decorator(login_required)
    def get(self, request, opt_in_id):
        opt_in = get_object_or_404(OptIn, pk=opt_in_id)
        attendee = Person.objects.get(user=request.user)
        OptIn.objects.get_or_create(attendee=attendee, sug_location=opt_in.sug_location, sug_time=opt_in.sug_time)
        return redirect(reverse('home'))
