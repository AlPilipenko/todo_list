from django.shortcuts import render, redirect
from django.http import HttpResponse

"importing different views:"
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

"To redirect user to a certain part af our app"
from django.urls import reverse_lazy


from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task


"custom method for user creations"
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class CustomLoginView(LoginView):
    "Since there is no model in this view we need to specify template"
    template_name = 'base/login.html'

    """
    LoginView provides us with a form, so just as with the modelviews
    we specify fields
    """
    fields = '__all__'

    "by default this is False. We want to redirect loged in users"
    redirect_authenticated_user = True

    """
    We will write redirect this time as a method.

    get_success_url()¶
        Determine the URL to redirect to when the form is successfully
        validated. Returns success_url by default.
    """

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    "Base functionality"
    template_name = 'base/register.html'
    "All the information in register template is provided by UserCreationForm"
    form_class = UserCreationForm  # 2
    "by default this is False. We want to redirect loged in users"
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):  # 1
        """
        1. Once post request is sent form valid method is triggered
        2. We submit this form (UserCreationForm)
        3. We get the user
        4. We log the user in directly and redirect the user to the ListView
           (login was the method we imported above)
        """
        user = form.save()  # 3
        if user is not None:
            # print("self.request, user" ,self.request, user)
            # >>> <WSGIRequest: POST '/register/'> testUser2
            login(self.request, user)  # 4
        "This finally validates form and reverse_lazy methof redirects user"
        return super(RegisterPage, self).form_valid(form)  # 4

    def get(self, *args, **kwargs):
        "We want to redirect loged in users"
        "redirect_authenticated_user not working here"
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


def test(request):
    return HttpResponse("Hello World")


class TaskList(LoginRequiredMixin, ListView):
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

    def get_context_data(self, **kwargs):
        """
        User specific data. This is how as user will get only his data.
        This will return:
        <QuerySet [<Task: Do>, <Task: Say Hi! (updated)>, <Task: Wash>,
        <Task: Clean>]>
        And it can be accessed in html: {{ tasks }} since we already assigned
        earlier context_object_name.
        """
        context = super().get_context_data(**kwargs)
        # print("111",context)

        context['tasks'] = context['tasks'].filter(user=self.request.user)
        # print(self.request.user) = sanita, snoozik

        # context['color'] = 'red'  - this is what this method does
        # we can access it in html - {{ color }}

        """Here we are filtering the filtered queryset already.
        Adding new key-value pair in context that will let user know number
        of incomplete items
        """
        context['count'] = context['tasks'].filter(complete=False).count()


        "Adding search functionality:"
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                                                # title__icontains=search_input)
                                                title__startswith=search_input)
        context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
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


class TaskCreate(LoginRequiredMixin, CreateView):
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
    # fields = '__all__'  # to list out all of the items of the field

    fields = ['title', 'description', 'complete']
    """
    After form is submitted we want to redirect user to a different page.
    So we need to set up success_url:
    """
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        """
        Triggered by default by POST request.
        Removes choice from the user to select user (user selection is made
        automatically) and it is the loged in user.
        """
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
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

    # fields = '__all__'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
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
