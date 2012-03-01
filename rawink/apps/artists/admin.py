from django.contrib import admin

from .models import *



class ArtistAdmin(admin.ModelAdmin):
    model = Artist
    # prepopulated_fields = {'slug': ("user.first_name", "user.last_name")}

class ArtistWorkPhotoAdmin(admin.ModelAdmin):
    model = ArtistWorkPhoto

admin.site.register(Artist, ArtistAdmin)
admin.site.register(ArtistWorkPhoto)
