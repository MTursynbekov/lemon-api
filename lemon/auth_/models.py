from django.contrib.auth.models import AbstractUser
from django.db import models

from auth_.managers import CustomUserManager
from utils.constants import USER_ROLES, USER_ROLE_CUSTOMER

from core.models import Product


class MainUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    role = models.SmallIntegerField(choices=USER_ROLES, default=USER_ROLE_CUSTOMER, verbose_name='Роль')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserProfile(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Product, verbose_name='Избранные')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
