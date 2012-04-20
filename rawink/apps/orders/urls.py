from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = patterns('',
    url(r'^$', OrderListView.as_view(), name="order-list"),
    url(r'^status-update/(?P<pk>\d*)$', OrderStatusChangeView, name="order-status-cahnge"),
    url(r'^new/$', CreateOrder.as_view(), name="create-order"),  
    url(r'^edit/(?P<pk>\d*)/$', EditOrder.as_view(), name="edit-order"),
    url(r'^detail/(?P<pk>\d*)/$', OrderDetail.as_view(), name="order-detail"),
    
    url(r'^bill/(?P<pk>\d*)$', OrderBillView, name="order-bill"),
    url(r'^artist/$', ArtistOrderList.as_view(), name="artist-order-list"),
    url(r'^artist/time/(?P<pk>\d*)$', OrderTimeList.as_view(), name="artist-order-time"),
    url(r'^artist/time-update/(?P<pk>\d*)$', OrderTimeUpdateView, name="artist-order-time-update"),
    url(r'^artist/update/(?P<pk>\d*)/$', OrderStatusUpdate.as_view(), name="artist-order-status-update"),
)
