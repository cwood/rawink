from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm as _UserCreationForm, \
    AuthenticationForm as _AuthenticationForm, \
    UserChangeForm as _UserChangeForm, \
    PasswordResetForm as _PasswordResetForm, \
    SetPasswordForm as _SetPasswordForm, \
    PasswordChangeForm as _PasswordChangeForm

from .fields import CreditCardField, ExpiryDateField, VerificationValueField

from .models import *


class UserForm(_UserCreationForm, forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'E-mail'
        
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',)
        
class AddressForm(forms.ModelForm):

    class Meta:
        model = Address

class CardForm(forms.ModelForm):
    number = CreditCardField(required=True)
    expiry_date = ExpiryDateField(required=True)
    security_code = VerificationValueField(required=True)
            
    class Meta:
        model = Card


class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        exclude = ('user', 'address', 'card')

class PasswordResetForm(_PasswordResetForm):
    pass


class SetPasswordForm(_SetPasswordForm):
    pass


class PasswordChangeForm(_PasswordChangeForm):
    pass
