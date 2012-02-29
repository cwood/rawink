from django.views.generic import CreateView, ListView, TemplateView, View
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


class CustomerView(TemplateView):
    template_name = 'customers/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(CustomerView, self).get_context_data(**kwargs)
        context['customer'] = Customer.objects.get(user=self.request.user)
        return context


class CustomerCard(CreateView):
    template_name = 'customers/card.html'
    form_class = CardForm
    success_message = 'Form Sent'
    fail_message = 'Failed!'
    success_url = '/customer/'

    def get_context_data(self, **kwargs):
        context = super(CustomerCard, self).get_context_data(**kwargs)
        context['contact_form_success'] = 'success' in self.request.GET
        context['success_message'] = self.success_message
        card_pk = self.kwargs.get('card_pk')
        context["customer"] = get_object_or_404(Customer, user = self.request.user)
        

        if card_pk:
            context["form"] = CardForm(instance=get_object_or_404(Card, pk=card_pk))
        return context

    # def get_success_url(self):
    #     return '%s?success' % self.request.path
    def get_initial(self):        
        initial = self.initial or {}
        context = self.get_context_data()
        customer = context['customer']

        initial.update({
        'first_name': customer.user.first_name,
        'last_name': customer.user.first_name,
            })
        return initial

    def form_valid(self, form):
        context = self.get_context_data()
        if (self.kwargs.get('card_pk')):
            self.object = form.save(commit=False)
            self.object.id=self.kwargs.get('card_pk')
            self.object.save()
        else:
            card_id = form.save()            
            user = self.request.user
            customer = Customer.objects.get(user=self.request.user)
            customer.card_id = card_id
            customer.save()        
        return redirect('/customer/')

class CustomerAddress(CreateView):
    template_name = 'customers/address.html'
    form_class = AddressForm
    success_message = 'Form Sent'
    fail_message = 'Failed!'
    success_url = '/customer/'

    def get_context_data(self, **kwargs):
        context = super(CustomerAddress, self).get_context_data(**kwargs)
        context['contact_form_success'] = 'success' in self.request.GET
        context['success_message'] = self.success_message
        address_pk = self.kwargs.get('address_pk')
        
        if address_pk:
            context["form"] = AddressForm(instance=get_object_or_404(Address, pk=address_pk))
        return context

    # def get_success_url(self):
    #     return '%s?success' % self.request.path

    def form_valid(self, form):
        context = self.get_context_data()
        if (self.kwargs.get('address_pk')):
            self.object = form.save(commit=False)
            self.object.id=self.kwargs.get('address_pk')
            self.object.save()
        else:
            address_id = form.save()            
            user = self.request.user
            customer = Customer.objects.get(user=self.request.user)
            customer.address_id = address_id
            customer.save()        
        return redirect('/customer/')
    
class CreateCustomer(CreateView):
    template_name = 'customers/customer.html'
    form_class = CustomerForm
    success_message = 'Form Sent'
    fail_message = 'Failed!'
    success_url = '/customer/'
    
    def get(self, request, *args, **kwargs):
        if self.request.user:
            print 'already logedin!!'
            return HttpResponseRedirect('/accounts/logout/')
        
        self.object = None
        return super(BaseCreateView, self).get(request, *args, **kwargs)

        
    def get_context_data(self, **kwargs):
        context = super(CreateCustomer, self).get_context_data(**kwargs)
        context['contact_form_success'] = 'success' in self.request.GET
        context['success_message'] = self.success_message
        
        if self.request.POST:
            context['user_form'] = UserForm(self.request.POST)
        else:
            context['user_form'] = UserForm()    
        return context

    # def get_success_url(self):
    #     return '%s?success' % self.request.path
    
    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        if user_form.is_valid() and form.is_valid():
            user = user_form.save()
            customer = form.save()

            g = Group.objects.get(name=_settings.CUSTOMER_GROUP)
            user.groups.add(g)
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
            response = super(CreateCustomer, self).form_valid(form)
        else:
            response = self.render_to_response(self.get_context_data(form=form))    
        return response
