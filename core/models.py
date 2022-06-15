from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=255, null=True)
    photo = models.ImageField()
    first_name = None
    last_name = None
    email = models.EmailField(null=True)
