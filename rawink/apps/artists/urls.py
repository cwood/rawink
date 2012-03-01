from django.conf.urls.defaults import *
from .views import *

artist_slug_list = '|'.join(Artist.objects.all().values_list('slug', flat=True))
slug_capture = '(?P<slug>%s)' % artist_slug_list

urlpatterns = patterns('',
    url(r'^$', ArtistIndex.as_view()),
    url(r'^%s/$' % slug_capture, ArtistDetail.as_view(), name='artist-detail'),
)
