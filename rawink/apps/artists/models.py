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


class Artist(models.Model):
    user = models.OneToOneField(User, null=True)
    slug = models.SlugField(max_length=100)
    day = models.CharField(_("Days Available"), max_length=255)
    bio = models.TextField(_('Bio'))
    title = models.CharField(_('Title'), max_length=100)
    photo = models.ImageField(upload_to='artists')    
    
    def __unicode__(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)
    
    def get_absolute_url(self):
        return reverse('artist-detail', kwargs=dict(slug=self.slug))    
        
class ArtistWorkPhoto(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True)
    original_image = models.ImageField(upload_to='galleries')    
    slug = AutoSlugField(max_length=100, populate_from='title')
    
    artist = models.ForeignKey(Artist, null=True)
    
    def __unicode__(self):
        return u'%s %s' % (self.artist, self.title)
        
    class Meta:
        verbose_name = 'Artist work Image'

