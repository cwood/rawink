# Artist Name - string
# username/login
# password
# Title/Position - string
# Days/Hours Avail - string
# Email
# Bio
# Gallery:
#   image
#   description

from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from autoslug import AutoSlugField
# from modeltools import Enum, format_filename as _ff, FilteredManager


from rawink.apps.galleries.models import Gallery, ImageModel

from imagekit.models import ImageSpec
from imagekit.processors import resize, Adjust
from imagekit.processors.crop import TrimBorderColor

class ArtistGalleryPhoto(ImageModel):
    url = models.CharField('link', max_length=200, default='', blank=True)

    class Meta:
        verbose_name = 'Artist work Image'


class ArtistGallery(Gallery):
    def __unicode__(self):
        return '%s\'s Photo Gallery' % self.title

    class GalleryMeta:
        member_models = [ArtistGalleryPhoto]

    class Meta:
        verbose_name_plural = 'Artist Works Galleries'

class Artist(models.Model):
    user = models.OneToOneField(User, null=True)
    gallery = models.OneToOneField(ArtistGallery, null=True)
    
    day = models.CharField(_("Day"), 
            max_length=255)
    bio = models.TextField(_('Bio'))

    def __unicode__(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)


