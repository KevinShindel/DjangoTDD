import uuid

from django.contrib.auth import user_logged_in
from django.contrib.auth.models import update_last_login
from django.db import models

# user_logged_in.disconnect(update_last_login)


class User(models.Model):
    email = models.EmailField(primary_key=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True


class Token(models.Model):
    ''' маркер '''
    email = models.EmailField()
    uid = models.CharField(max_length=40, default=uuid.uuid4)
