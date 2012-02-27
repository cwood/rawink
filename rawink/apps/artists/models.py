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
    
    day = models.CharField(_("Day"), 
            max_length=255)
    bio = models.TextField(_('Bio'))

    def __unicode__(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)
