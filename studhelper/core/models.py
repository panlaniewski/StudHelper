from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # AbstractUser уже содержит: username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined
    email = models.EmailField('email address', unique=True)
    is_email_verified = models.BooleanField(default=False)


    

