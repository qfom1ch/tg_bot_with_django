from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=255, unique=True, null=False, blank=False, verbose_name='Телефон')
    tg_user_id = models.IntegerField()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
