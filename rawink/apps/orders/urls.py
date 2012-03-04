from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = patterns('',
    url(r'^$', login_required(OrderView.as_view()), name="order"),  
    url(r'^new/$', login_required(CreateOrder.as_view()), name="create-order"),  
    url(r'^edit/(?P<pk>\d*)/$', login_required(CreateOrder.as_view()), name="edit-order"),
    url(r'^detail/$', login_required(OrderDetail.as_view()), name="order-detail"),
    url(r'^artist/$', login_required(ArtistOrderList.as_view()), name="artist-order-list"),
    url(r'^update/artist/(?P<pk>\d*)/$', login_required(OrderStatusUpdate.as_view()), name="artist-order-status-update"),
)