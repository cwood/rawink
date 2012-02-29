from django.contrib import admin

from .models import *



class ArtistAdmin(admin.ModelAdmin):
    model = Artist

admin.site.register(Artist, ArtistAdmin)


from django.contrib import admin

from rawink.apps.galleries.admin import register_gallery_admin
from .models import ArtistGallery, ArtistGalleryPhoto

class ArtistGalleryPhotoAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'original_image':
            kwargs['help_text'] = 'Please upload 950pxX379px to get best user experience '
        return super(ArtistGalleryPhotoAdmin,self).formfield_for_dbfield(db_field,**kwargs)
           
register_gallery_admin( ArtistGallery)
admin.site.unregister(ArtistGalleryPhoto)
admin.site.register(ArtistGalleryPhoto, ArtistGalleryPhotoAdmin)