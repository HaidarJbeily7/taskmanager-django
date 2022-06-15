from django.db import models
from taskmanager.settings import AUTH_USER_MODEL

# Create your models here.


class List(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)


class PriorityType(models.TextChoices):
    p1 = "P1"
    p2 = "P2"
    p3 = "P3"

class Task(models.Model):
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    due_datetime = models.DateTimeField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    priority = models.CharField(max_length=255, choices=PriorityType.choices, null=True, blank=True)
    parent_task = models.ForeignKey('Task', on_delete=models.CASCADE, null=True, blank=True)

