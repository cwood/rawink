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
from django.core.exceptions import ValidationError

class UserForm(_UserCreationForm, forms.ModelForm):
    
    username = forms.EmailField(max_length=64,
                                    help_text="The person's email address.")
                                    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',)
        
    def clean_email(self):
            email = self.cleaned_data['username']
            return email    

class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        exclude = ('customer', )

class CardForm(forms.ModelForm):
    number = CreditCardField(required=True)
    expiry_date = ExpiryDateField(required=True)
    security_code = VerificationValueField(required=True)
            
    class Meta:
        model = Card
        exclude = ('customer',)
        
    # def validate_unique(self):
    #     exclude = self._get_validation_exclusions()
    #     exclude.remove('customer') # allow checking against the missing attribute
    #     try:
    #         self.instance.validate_unique(exclude=exclude)
    #     except ValidationError, e:
    #         self._update_errors(e.message_dict)


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
