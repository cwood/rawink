from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = patterns('',
    url(r'^$', CustomerView.as_view(), name="customer"),  
    url(r'^new/$', CreateCustomer.as_view(), name="create-customer"),  
    url(r'^address/add/$', CreateAddress.as_view(), name="add-address-customer"),
    url(r'^address/(?P<pk>[0-9]+)/$', EditAddress.as_view(), name="edit-address-customer"),
    url(r'^card/add/$', CreateCard.as_view(), name="add-card-customer"),
    url(r'^card/(?P<pk>[0-9]+)/$', EditCard.as_view(), name="edit-card-customer"),

)
