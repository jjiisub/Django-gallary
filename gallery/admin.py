from django.contrib import admin

from .models import Artist, Artwork, Exhibition

# Register your models here.

admin.site.register(Artist)
admin.site.register(Artwork)
admin.site.register(Exhibition)
