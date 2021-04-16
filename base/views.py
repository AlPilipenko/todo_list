from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Task


def test(request):
    return HttpResponse("Hello World")


class TaskList(ListView):
    """
    We are inhereting from ListView.
    We don't need to connect html template to this view.
    Django is already looking for task_list.html.
    """
    model = Task

    """
    Now we want to render out data in our template. How Django passes queryset
    into template?
    By default Django calls the query - object_list
    But we can change it:
    """

    context_object_name = 'tasks'


class Fr(DetailView):
    """
    Returns information about simple items.
    So when we click on the task we want more information about this item.
    """
