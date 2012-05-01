import datetime

from django.views.generic import CreateView, UpdateView, ListView, DetailView, TemplateView, FormView, View
from django.conf import settings
from django.utils import translation
from django.utils import simplejson as json
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed
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
    paginate_by = settings.PAGINATE_BY or 10 
    
    def get(self, request, *args, **kwargs):
        get = super(OrderListView, self).get(request, *args, **kwargs)
        print self.request.session.get('usergroup')
        if self.request.session.get('usergroup') in ('admin', 'artist',):
            return get
        else:
            return HttpResponseRedirect(reverse('logout'))
        
    def get_queryset(self, **kwargs):
        qs = super(OrderListView, self).get_queryset(**kwargs)
        if self.request.GET.get('token'):
            qs = qs.filter(token=self.request.GET.get('token'))
        
        if self.request.GET.get('date'):
            if self.request.GET.get('date') == 'today':
                date_min = datetime.datetime.combine(datetime.datetime.today(), datetime.time.min)
                date_max = datetime.datetime.combine(datetime.datetime.today(), datetime.time.max)            
            elif self.request.GET.get('date') == 'yesterday':
                yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
                date_min = datetime.datetime.combine(yesterday, datetime.time.min)
                date_max = datetime.datetime.combine(yesterday, datetime.time.max)            
            else:
                date = datetime.datetime.strptime(self.request.GET.get('date'), '%m-%d-%Y')
                date_min = datetime.datetime.combine(date, datetime.time.min)
                date_max = datetime.datetime.combine(date, datetime.time.max)            
            qs = qs.filter(created__range=(date_min, date_max))
        return qs


    
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
            'customer' : customer,
            'product' : product,
        })
                        
        return initial

    def form_valid(self, form):
        if form.is_valid():
            order = form.save()
            url = self.request.path
            if order:
            
                token = order.token
                url = '%s?token=%s&success' % (self.request.path, order.token)                
                return HttpResponseRedirect(url)
        else:
            response = super(CreateOrder, self).form_valid(form)    


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
        qs = Order.objects.all().filter(product__artist__user=self.request.user)

        date_min = datetime.datetime.combine(datetime.datetime.today(), datetime.time.min)
        date_max = datetime.datetime.combine(datetime.datetime.today(), datetime.time.max)            
        qs = qs.filter(created__range=(date_min, date_max))
        
        return qs

    def get_context_data(self, **kwargs):
        context = super(ArtistOrderList, self).get_context_data(**kwargs)
        return context

class OrderConfirm(LoginRequiredMixin, UpdateView):
    template_name = 'orders/status_update.html'
    form_class = OrderStatusPriceUpdateForm
    model = Order
    success_url = '/order/artist/time/%d'
    
    def get_success_url(self):
        return self.success_url % (self.object.id)
        
    def get_initial(self):        
        initial = self.initial or {}
        payment_rate = self.request.POST.get('payment_rate')

        if payment_rate is None or payment_rate == 0:
            payment_rate = settings.PAYMENT_RATE

        initial.update({
            'payment_rate' : payment_rate,
            'status' : 'confirmed',
        })
        return initial
        

class OrderTimeList(LoginRequiredMixin, DetailView):
    template_name = 'orders/order_time_list.html'
    model = Order
    
    def get_context_data(self, **kwargs):
        context = super(OrderTimeList, self).get_context_data(**kwargs)
        
        order = self.get_object()
        if not order.ordertime_set.all().filter(stop__isnull=True).order_by('-id')[:1].count():
            context.update({'can_start': True})
        context.update({'total_time':_sum_timedelta(order.id)})
        return context    


def OrderTimeUpdateView(request, pk):
    rdict = {'save': False}
    if request.method == 'GET':
        is_saved = None
        try:
            order = Order.objects.get(id=pk)
            if order:
                if request.GET.get('action') == 'start':
                    if order.ordertime_set.all().filter(stop__isnull=True).order_by('-id')[:1].count() == 0:
                        if order.status=='confirmed':
                            order.status='in-progress'
                            order.save()
                        sw = StopWatch.objects.create()
                        order_time = OrderTime(order=order, stop_watch=sw, start=datetime.datetime.now())
                        is_saved = order_time.save()
                        rdict.update({'save': True }) 

                elif request.GET.get('action') == 'stop':
                    order_time = order.ordertime_set.all().filter(stop__isnull=True).order_by('-id')
                    if order_time[:1].count():
                        order_time = order_time[0]
                        order_time.stop=datetime.datetime.now()
                        is_saved = order_time.save()
                        rdict.update({'save': True}) 
        except:
            pass
        json = simplejson.dumps(rdict, ensure_ascii=False)
            # And send it off.
        return HttpResponse( json, mimetype='application/javascript')
    else:
        return HttpResponseNotAllowed(['POST','GET'])

def OrderBillView(request, pk):
    rdict = {'save': False}
    if request.method == 'POST':
        order = Order.objects.get(pk=pk)
        if order.status == 'completed':
            form = OrderBillFrom(request.POST, instance=order)
            if form.is_valid():
                form.save()
                rdict.update({'save': True}) 

        json = simplejson.dumps(rdict, ensure_ascii=False)
            # And send it off.
        return HttpResponse( json, mimetype='application/javascript')
    else:
        return HttpResponseNotAllowed(['POST','GET'])

def OrderStatusChangeView(request, pk):
    rdict = {'save': False}
    if request.method == 'GET':
        order = Order.objects.get(pk=pk)
        form = OrderStatusUpdateFrom(request.GET, instance=order)
        if form.is_valid():
            if request.GET.get('status') == 'completed':
                form = form.save(commit=False)
                form.total_time=_sum_timedelta(order.id)

            rdict.update({'save': True, 'status': request.GET.get('status')}) 
            form.save()

        json = simplejson.dumps(rdict, ensure_ascii=False)
            # And send it off.
        return HttpResponse( json, mimetype='application/javascript')
    else:
        return HttpResponseNotAllowed(['POST','GET'])

import datetime
from time import mktime

def _sum_timedelta(order):
    total_time = 0
    try:
        order = Order.objects.get(pk=order)
        sw = order.ordertime_set.all()
        for s in sw:
            time_diff = 0
            if s.stop and s.start:
                time_diff = mktime(s.stop.timetuple())-mktime(s.start.timetuple())
            total_time +=time_diff
        return round(total_time/(60*60),2)    
    except:
        return 0
    