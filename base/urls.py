# how we create url patterns here
from django.urls import path  # importing path function
from . import views  # when we add new views they will be added here
from .views import TaskList


"""
Once we have actuoal view in the view we can add them here
Our URL resolver can't use classes inside, therefore we need to use
as_view method
"""

urlpatterns = [
    path('/test', views.test, name='test'),
    path('', TaskList.as_view(), name='tasks'),
]
