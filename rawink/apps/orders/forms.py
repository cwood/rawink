from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm as _UserCreationForm, \
    AuthenticationForm as _AuthenticationForm, \
    UserChangeForm as _UserChangeForm, \
    PasswordResetForm as _PasswordResetForm, \
    SetPasswordForm as _SetPasswordForm, \
    PasswordChangeForm as _PasswordChangeForm

from django.forms import RadioSelect, HiddenInput

from .models import Order


class UserForm(_UserCreationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',)


class OrderForm(forms.ModelForm):
    is_agree = forms.BooleanField(label='I have read and agree to the terms of the above release form')

    class Meta:
        model = Order
        fields = ('product', 'customer', 'date_for_tattoo', 'note', )


class OrderStatusPriceUpdateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('status', 'payment_type', 'payment_rate',)
        widgets = {
            'payment_type': RadioSelect,
            'status': HiddenInput,
        }


class OrderStatusUpdateFrom(OrderForm):

    class Meta:
        model = Order
        fields = ('status',)


class OrderCompletedFrom(OrderForm):
    class Meta:
        model = Order
        fields = ('status',)


class OrderBillFrom(OrderForm):
    class Meta:
        model = Order
        fields = ('payment_price', 'status',)

