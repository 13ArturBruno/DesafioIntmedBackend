from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField('Usuário', max_length=60, unique=True)
    email = models.CharField('Email', max_length=100)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

