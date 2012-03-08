from django.views.generic import CreateView, UpdateView, ListView, TemplateView, View
from django.conf import settings
from django.utils import translation
from django.utils import simplejson as json
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, redirect

from .forms import *
from .models import Customer, Address
import settings as _settings
from django.contrib.auth.models import Group

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

from rawink.apps.main.mixins import LoginRequiredMixin

class CustomerView(LoginRequiredMixin, TemplateView):
    template_name = 'customers/index.html'
    
    def get_context_data(self, **kwargs):
        if self.request.session.get('usergroup') == 'customer':
            context = super(CustomerView, self).get_context_data(**kwargs)
            context['customer'] = get_object_or_404(Customer, user=self.request.user)
            return context
        else:
            return logout(self.request)



class CreateCard(LoginRequiredMixin, CreateView):
    form_class = CardForm
    success_url = '/customer/'
    template_name = 'customers/card_form.html'

    def get_success_url(self):
        return self.success_url
                
    def get_initial(self):        
        initial = self.initial or {}
        initial.update({
        'first_name': self.request.user.first_name,
        'last_name': self.request.user.first_name,
        'customer': Customer.objects.get(user = self.request.user),
            })
        return initial

    def form_valid(self, form):
        context = self.get_context_data()
        card = form.save(commit=False)

        customer = Customer.objects.get(user=self.request.user)
        card.customer = customer
        return super(CreateCard, self).form_valid(card)

class EditCard(LoginRequiredMixin, UpdateView):
    form_class = CardForm
    model = Card
    success_url = "/customer/"

class CreateAddress(LoginRequiredMixin, CreateView):
    form_class = AddressForm
    success_url = '/customer/'
    template_name = 'customers/address_form.html'
    
    def get_success_url(self):
        return self.success_url

    def get_initial(self):        
        initial = self.initial or {}
        initial.update({
        'first_name': self.request.user.first_name,
        'last_name': self.request.user.first_name,
        'customer': Customer.objects.get(user = self.request.user),
            })
        return initial

    def form_valid(self, form):
        context = self.get_context_data()
        card = form.save(commit=False)

        customer = Customer.objects.get(user=self.request.user)
        card.customer = customer
        return super(CreateAddress, self).form_valid(card)

class EditAddress(LoginRequiredMixin, UpdateView):
    form_class = AddressForm
    model = Address
    success_url = "/customer/"



class CreateCustomer(CreateView):
    template_name = 'customers/customer_form.html'
    form_class = CustomerForm
    success_url = '/customer/'
    
    def get(self, request, *args, **kwargs):
        print self.request.user
        if self.request.user == 'AnonymousUser':
            print 'already logedin!!'
            return HttpResponseRedirect('/accounts/logout/')
        
        self.object = None
        return super(CreateCustomer, self).get(request, *args, **kwargs)

        
    def get_context_data(self, **kwargs):
        context = super(CreateCustomer, self).get_context_data(**kwargs)
        
        if self.request.POST:
            context['user_form'] = UserForm(self.request.POST)
        else:
            context['user_form'] = UserForm()    
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        if user_form.is_valid() and form.is_valid():
            user = user_form.save()
            customer = form.save(commit=False)

            g = Group.objects.get(name=_settings.CUSTOMER_GROUP)
            user.groups.add(g)
            user.email = user.username
            user.save()
            
            customer.user_id = user.id
            customer.save()
                        
            u = authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password1'])
            if u is not None:
                if u.is_active:
                    print 'User login!'
                    login(self.request, u)
                    # Redirect to a success page.
                else:
                    print 'User disabled!!'
                    # Return a 'disabled account' error message
            else:
                print 'User disabled!!'
            return HttpResponseRedirect(self.request.META.get('http_referer'))
        else:
            response = self.render_to_response(self.get_context_data(form=form))    
        return response

class EditCustomer(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    success_url = '/customer/'

