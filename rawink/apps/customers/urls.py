from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = patterns('',
    url(r'^$', login_required(CustomerView.as_view())),  
    url(r'^new/$', CreateCustomer.as_view(), name="create-customer"),  
    url(r'^address/add/$', login_required(CustomerAddress.as_view()), name="add-address-customer"),
    url(r'^address/(?P<address_pk>[0-9]+)/edit/$', login_required(CustomerAddress.as_view()), name="edit-address-customer"),
    url(r'^card/add/$', CustomerCard.as_view(), name="add-card-customer"),
    url(r'^card/(?P<card_pk>[0-9]+)/edit/$', CustomerCard.as_view(), name="edit-card-customer"),

)
