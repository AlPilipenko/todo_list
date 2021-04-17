from django.shortcuts import render
from django.http import HttpResponse

"importing different views:"
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

"To redirect user to a certain part af our app"
from django.urls import reverse_lazy

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


class TaskDetail(DetailView):
    """
    Returns information about simple items.
    So when we click on the task we want more information about this item.
    """
    model = Task
    context_object_name = 'task'

    """
    By default this view is looking for a model name + prefix _detail, which
    is task_detail.html
    To costumize template name for django to look for
    """
    template_name = 'base/task.html'


class TaskCreate(CreateView):
    """
    It has more complex logic than previous view, because we are sending post
    requests and we have to create an item.
    """
    model = Task
    "Not changing template name here because it will mess up TaskUpdate"
    # template_name = 'base/task-create.html'

    """
    By default the CreateView already giving us a model (Task) Form to work with.
    Model form - a class representation of a form based on a model. That means
    it going to take "Task" model and its going to create all the fields by
    default for us. So we only need to specify the fields that we want.
    """

    # field = ['title', 'desctiption']
    fields = '__all__'  # to list out all of the items of the field

    """
    After form is submitted we want to redirect user to a different page.
    So we need to set up success_url:
    """
    success_url = reverse_lazy('tasks')


class TaskUpdate(UpdateView):
    """
    UpdateView takes an item, prefills the form and one submited modifies data.
    """
    model = Task

    """
    By default this view is also looking for a model name + prefix _form,
    since we already have this template - task_form.html we don't need to
    create another one.
    """
    # template_name = 'base/task-update.html'

    fields = '__all__'
    success_url = reverse_lazy('tasks')


class TaskDelete(DeleteView):
    """
    It does two thigs: 1)Renders a page that says "are you sure"?
                       2)And if wish to process it will send a post request and
                         it will delete the item.
    """

    model = Task

    "By default context_object_name is 'object', so we'll change it to task"
    context_object_name = 'task'

    "By default DeleteView is looking for a model(Task) + _confirm_delete.html"

    success_url = reverse_lazy('tasks')
