from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm as _UserCreationForm, \
    AuthenticationForm as _AuthenticationForm, \
    UserChangeForm as _UserChangeForm, \
    PasswordResetForm as _PasswordResetForm, \
    SetPasswordForm as _SetPasswordForm, \
    PasswordChangeForm as _PasswordChangeForm


from .models import Order

from registration.forms import RegistrationFormUniqueEmail as _RegistrationFormUniqueEmail

class UserForm(_UserCreationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',)
        
class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        exclude = ('user', 'token',)

