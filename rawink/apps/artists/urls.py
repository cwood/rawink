from django.conf.urls.defaults import *
from .views import *

urlpatterns = patterns('',
    url(r'^$', ArtistIndex.as_view(), name="artist-index"),
    url(r'^(?P<slug>[-\w]+)/$', ArtistDetail.as_view(), name='artist-detail'),
)
