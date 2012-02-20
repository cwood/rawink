from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # (r'^tinymce/', include('tinymce.urls')),

    # (r'^$', include('rawink.apps.main.urls')),

)
