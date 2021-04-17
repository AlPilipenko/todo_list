# how we create url patterns here
from django.urls import path  # importing path function
from . import views  # when we add new views they will be added here
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete


"""
Once we have actuoal view in the view we can add them here
Our URL resolver can't use classes inside, therefore we need to use
as_view method
"""

urlpatterns = [
    path('test/', views.test, name='test'),  # dynamic way to access URLs
    path('', TaskList.as_view(), name='tasks'),

    # "this view by default looks for PRIMARY_KEY value (pk-value)"
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),

    #
    path('task-create/', TaskCreate.as_view(), name='task-create'),

    # Here we also need PRIMARY_KEY so that Django knows what task we updating
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),

]
