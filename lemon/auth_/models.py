from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    address = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True, max_length=20)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


@receiver(post_save, sender=MainUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=MainUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
