from django.contrib import admin

from auth_ import models

admin.site.register(models.MainUser)
admin.site.register(models.UserProfile)
