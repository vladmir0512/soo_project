from django.contrib import admin
from . import models

admin.site.register(models.Post)
admin.site.register(models.Person)
admin.site.register(models.Comment)
admin.site.register(models.Toxic_Comment)
admin.site.register(models.Toxic_Post)

# Register your models here.
