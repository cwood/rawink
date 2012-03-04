from django.views.generic import CreateView, UpdateView, ListView, DetailView, TemplateView, FormView, View
from django.conf import settings
from django.utils import translation
from django.utils import simplejson as json
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, redirect

from .forms import *
from .models import *
from rawink.apps.customers.models import Customer
from rawink.apps.artists.models import ArtistWorkPhoto

from django.contrib.auth.models import Group

from django.contrib.auth import authenticate, login


class OrderView(ListView):
    template_name = 'orders/order_list.html'
    model = Order
    

class OrderDetail(TemplateView):
    template_name = 'orders/order_detail.html'
    model = Order

    def get(self, *args, **kwargs):
        action = self.request.GET.get('action')
        order = self.request.GET.get('order')
        if action == 'statuschange':
            redirect_url = reverse('artist-order-status-update')
            extra_params = "?order=%s&action=%s" % (order, action)
            full_url = "%s%s" % (redirect_url, extra_params)
            return redirect(full_url)

    def get_context_data(self, **kwargs):
        context = super(OrderDetail, self).get_context_data(**kwargs)
        context['order'] = get_object_or_404(Order, token=self.request.GET.get('order'))
        return context


class CreateOrder(CreateView):
    template_name = 'orders/order.html'
    form_class = OrderForm
    success_message = 'Form Sent'
    fail_message = 'Failed!'
    success_url = '/order/'

    
    def get_initial(self):        
        initial = self.initial or {}
        context = self.get_context_data()
        customer = get_object_or_404(Customer, user = self.request.user)
    
        if self.request.GET.get('product'):
            initial.update({
            'product' : get_object_or_404(ArtistWorkPhoto, slug=self.request.GET.get('product')).id,
            })
        
        initial.update({
        'billing_first_name': customer.user.first_name,
        'billing_last_name': customer.user.first_name,
        'billing_street_address_1': customer.address.street,
        'billing_state': customer.address.state,
        'billing_postal_code': customer.address.zip_code,
        'billing_phone': customer.phone,
        'payment_card': customer.card.number,
            })
        return initial

    def form_valid(self, form):
        order = form.save(commit=False)
        order.user = self.request.user
        return super(CreateView, self).form_valid(form)


class ArtistOrderList(OrderView):
    def get_queryset(self):
        print self.request.user
        qs = Order.objects.all().filter(product__artist__user=self.request.user)
        qs.query.group_by = ['status']
        return qs

    def get_context_data(self, **kwargs):
        context = super(ArtistOrderList, self).get_context_data(**kwargs)
        return context

class OrderStatusUpdate(UpdateView):
    template_name = 'orders/status_update.html'
    form_class = OrderStatusUpdate
    model = Order
    success_url = '/order/artist'
