from django.contrib import admin

from .models import *

class ArtistWorkPhotoTabularInline(admin.TabularInline):
    model = ArtistWorkPhoto


class ArtistAdmin(admin.ModelAdmin):
    model = Artist
    # prepopulated_fields = {'slug': ("user.first_name", "user.last_name")}
    inlines = [ArtistWorkPhotoTabularInline,]

admin.site.register(Artist, ArtistAdmin)

