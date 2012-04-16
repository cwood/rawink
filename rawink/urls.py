from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView

from rawink.apps.main.views import LoginView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # (r'^tinymce/', include('tinymce.urls')),

    (r'^$', include('rawink.apps.artists.urls')),
    
    (r'^customer/', include('rawink.apps.customers.urls')),
    (r'^artist/', include('rawink.apps.artists.urls')),
    (r'^order/', include('rawink.apps.orders.urls')),
    
    url(r'^accounts/login/$', LoginView.as_view(), name='login'),
    # url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'main/user.html'}, name="login"),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page':'/customer/',}),
    
)
