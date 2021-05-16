from django.contrib.auth.models import AbstractUser
from django.db import models
from auth_.managers import CustomUserManager
from utils.constants import USER_ROLES, USER_ROLE_CUSTOMER

from core.models import Product
from utils.validators import validate_phone_number


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
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE, related_name="profile")
    address = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True, max_length=20, validators=[validate_phone_number, ])

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
