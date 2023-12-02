from django.contrib import admin

from .models import Applyment, User

# Register your models here.

admin.site.register(User)
admin.site.register(Applyment)