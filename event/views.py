from django.shortcuts import render

from .models import Event

# Create your views here.
def event_list(request):

    event_list = Event.objects.all()
    times = [ time for time in range(8, 20)]

    return render(request, 'event/event_list.html', {
            'event_list':event_list,
            'times':times,
        })