from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = patterns('',
    url(r'^$', login_required(OrderListView.as_view()), name="order"),
    url(r'^status-update/(?P<pk>\d*)$', login_required(OrderStatusChangeView), name="order-status-cahnge"),
    url(r'^new/$', login_required(CreateOrder.as_view()), name="create-order"),  
    url(r'^edit/(?P<pk>\d*)/$', login_required(EditOrder.as_view()), name="edit-order"),
    url(r'^detail/(?P<pk>\d*)/$', login_required(OrderDetail.as_view()), name="order-detail"),
    url(r'^artist/$', login_required(ArtistOrderList.as_view()), name="artist-order-list"),
    url(r'^update/artist/(?P<pk>\d*)/$', login_required(OrderStatusUpdate.as_view()), name="artist-order-status-update"),
)
