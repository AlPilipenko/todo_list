from django.db import models
from django.contrib.auth.models import User
"""This User model taking care of User information such as username, emails,
passwords, etc. This is how Django handles authentication.
"""


class Task(models.Model):
    "Foreign_key creates one-to-many relationship"
    "If user is deleted his task are also deleted - CASCADE"
    "If user is deleted his task is remained - SET_NULL"
    "null=True - in theory this could be empty field"
    "blank=True - when we submit a form this can also be empty"
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    "For a string field"
    title = models.CharField(max_length=200)

    "For a string field but with more options"
    description = models.TextField(null=True, blank=True)

    "To have True or False value in DB"
    complete = models.BooleanField(default=False)

    "When we need date and time of creation to be auto populated"
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        "To create string representation of the model"
        return self.title

    """This is how to order a queryset. When we returning multiple items
    Model.objects.filter() - we can order returned objects by their completion
    status
    """
    class Meta:
        ordering = ['complete']
