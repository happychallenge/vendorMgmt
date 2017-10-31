from datetime import date, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Event

# Create your views here.
@login_required
def event_list(request):
    today = date.today()
    from_dt = today + timedelta(days=-90)
    to_dt = today + timedelta(days=90)

    event_list = Event.objects.filter(event_date__range=[from_dt, to_dt]).order_by('event_date')
    times = [ time for time in range(10, 20)]

    return render(request, 'event/event_list.html', {
            'event_list':event_list,
            'times':times,
        })


@login_required
def event_timetable(request):
    today = date.today()
    from_dt = today + timedelta(days=-90)
    to_dt = today + timedelta(days=90)

    event_list = Event.objects.filter(event_date__range=[from_dt, to_dt]).order_by('event_date')

    return render(request, 'event/event_timetable.html', {
            'event_list':event_list,
        })