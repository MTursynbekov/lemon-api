from django.db.models.signals import post_save
from django.dispatch import receiver

from auth_.models import MainUser, UserProfile


@receiver(post_save, sender=MainUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=MainUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

