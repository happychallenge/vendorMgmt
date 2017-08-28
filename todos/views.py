from datetime import date, timedelta

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from decorators import ajax_required

from .models import Todo
from .forms import TodoForm

# Create your views here.
def todo_list(request):
    today = date.today()
    from_dt = today + timedelta(days=-7)
    to_dt = today + timedelta(days=90)

    todo_list = Todo.objects.filter(duedate__range=[from_dt, to_dt]).order_by('duedate')
    times = [ time for time in range(8, 20)]

    return render(request, 'todos/todo_list.html', {
            'todo_list': todo_list,
            'times': times,
        })

def todo_detail(request, id):

    todo = Todo.objects.get(id=id)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)

        if form.is_valid():
            form.save()
            return redirect('todos:todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todos/todo_detail.html', {
            'form': form,
        })


@ajax_required
def ajax_todo_add(request):
    data = dict()
    if request.method == 'POST':
        form = TodoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('todos:todo_list')

        date['form_is_valid'] = False

    else:
        form = TodoForm()

    data['html_form'] = render_to_string('todos/ajax_todo_add.html', {'form':form}, request=request)
    return JsonResponse(data)