from django.db import models
from taskmanager.settings import AUTH_USER_MODEL
from .managers import SoftDeleteManager

class SofDeleteModel(models.Model):

    is_deleted = models.BooleanField(default=False)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True


class List(SofDeleteModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)


class PriorityType(models.TextChoices):
    p1 = "P1"
    p2 = "P2"
    p3 = "P3"


class Task(SofDeleteModel):
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    due_datetime = models.DateTimeField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    priority = models.CharField(max_length=255, choices=PriorityType.choices, null=True, blank=True)
    parent_task = models.ForeignKey('Task', on_delete=models.CASCADE, null=True, blank=True)

