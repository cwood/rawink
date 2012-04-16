from django.views.generic import CreateView, UpdateView, ListView, DetailView, TemplateView, FormView, View
from django.conf import settings
from django.utils import translation
from django.utils import simplejson as json
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, redirect
from django.utils import simplejson

from .forms import *
from .models import *
from rawink.apps.customers.models import Customer
from rawink.apps.artists.models import ArtistWorkPhoto

from django.contrib.auth.models import Group

from django.contrib.auth import authenticate, login

from rawink.apps.main.mixins import LoginRequiredMixin

class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'orders/order_list.html'
    model = Order
    
    def get_queryset(self):
        return Order.objects.all().filter()

def OrderStatusChangeView(request, pk):

    if request.method == 'GET':
        order = Order.objects.get(pk=pk)
        form = OrderStatusUpdateFrom(request.GET, instance=order)
        
        clean = form.is_valid()
        rdict = {'save': False}

        if clean:
            rdict.update({'save': True}) 
            form.save()

        json = simplejson.dumps(rdict, ensure_ascii=False)
            # And send it off.
        return HttpResponse( json, mimetype='application/javascript')
    else:
        return HttpResponseNotAllowed(['POST','GET'])

    
class CreateOrder(LoginRequiredMixin, CreateView):
    template_name = 'orders/order.html'
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        if self.request.GET.get('product'):    
            product = get_object_or_404(ArtistWorkPhoto, slug=self.request.GET.get('product'))
            context.update({"product": product})
        elif self.request.GET.get('token'):
            order = get_object_or_404(Order, token=self.request.GET.get('token'))
            context.update({"order": order, 'product': order.product})
            
        context['order_created_success'] = 'success' in self.request.GET
        return context

    def get_success_url(self):
        return '%s?success' % (self.request.path)
        
    def get_initial(self):        
        initial = self.initial or {}
        context = self.get_context_data()
        customer = None
        product = None
        
        if self.request.user:
            customer = get_object_or_404(Customer, user = self.request.user)
        if self.request.GET.get('product'):
            product = get_object_or_404(ArtistWorkPhoto, slug=self.request.GET.get('product'))
            
        initial.update({
            'customer' :customer,
            'product' :product,
        })
                        
        return initial

    def form_valid(self, form):
        order = form.save()
        url = self.request.path
        if order:
        # response = super(CreateOrder, self).form_valid(form)
            token = order.token
            url = '%s?token=%s&success' % (self.request.path, order.token)

        return HttpResponseRedirect(url)


class OrderDetail(LoginRequiredMixin, DetailView):
    template_name = 'orders/order_detail.html'
    model = Order

    def get_queryset(self, **kwargs):
        qs = super(OrderDetail, self).get_queryset(**kwargs)
        
        if self.request.session.get('usergroup') == 'artist':
            qs = qs.filter(product__artist__user = self.request.user)
        else:
            qs = qs.filter(customer= Customer.objects.get(user=self.request.user))
        return qs

class EditOrder(LoginRequiredMixin, UpdateView):

    model = Order
    form_class = OrderForm
    template_name = 'orders/order.html'

    def get_queryset(self, **kwargs):
        qs = super(EditOrder, self).get_queryset(**kwargs)
        return qs.filter(customer= Customer.objects.get(user=self.request.user))

class ArtistOrderList(OrderListView):
    template_name = 'orders/artist_order_list.html'
    
    def get_queryset(self):
        qs = Order.objects.all().filter(product__artist__user=self.request.user).filter(status='pending')
        # qs.query.group_by = ['status']
        return qs

    def get_context_data(self, **kwargs):
        context = super(ArtistOrderList, self).get_context_data(**kwargs)
        return context

class OrderStatusUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'orders/status_update.html'
    form_class = OrderStatusPriceUpdateForm
    model = Order
    success_url = '/order/artist'
