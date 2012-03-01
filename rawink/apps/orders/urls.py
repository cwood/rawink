from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = patterns('',
    url(r'^$', login_required(OrderView.as_view()), name="order"),  
    url(r'^new/$', login_required(CreateOrder.as_view()), name="create-order"),  
    url(r'^edit/(?P<order_pk>[0-9]+)/$', login_required(CreateOrder.as_view()), name="edit-order"),
)
