from django.contrib import admin

from .models import article
from django.contrib.auth.models import Permission
# Register your models here.

admin.site.register(article)
admin.site.register(Permission)