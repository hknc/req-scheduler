from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Default user."""

    # give admin panel access to default users
    is_staff = models.BooleanField(default=True)
