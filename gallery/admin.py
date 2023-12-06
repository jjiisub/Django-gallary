from django.contrib import admin

from .models import Artist, Artwork, Exhibition

admin.site.register(Artist)
admin.site.register(Artwork)
admin.site.register(Exhibition)
