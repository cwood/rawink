from django.views.generic import CreateView, ListView, TemplateView, View
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


class OrderView(TemplateView):
    template_name = 'orders/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['customer'] = Customer.objects.get(user=self.request.user)
        return context


class CreateOrder(CreateView):
    template_name = 'orders/order.html'
    form_class = OrderForm
    success_message = 'Form Sent'
    fail_message = 'Failed!'
    success_url = '/order/'

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        order_pk = self.kwargs.get('order_pk')
        
        context["customer"] = get_object_or_404(Customer, user = self.request.user)       

        if order_pk:
            context["form"] = OrderForm(instance=get_object_or_404(Order, pk=order_pk))
        return context

    def get_initial(self):        
        initial = self.initial or {}
        context = self.get_context_data()
        customer = context['customer']

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

