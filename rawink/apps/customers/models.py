# Customer Name
# - Optional: Guardian (yes/no)
# - Current Date (auto updated when account is created/updated)
# - Email Address
# - Phone Number
# - Street Address, City / State / Zip
# - Birthday
# - Optional (if Guardian = yes) : Person to be tattooed birthday
# - Digital Signature
# - Checkbox agreement to pay deposit amount
# - Checkbox if card holder is the above customer
# Optional: If card holder is NOT the above customer
# - Card Holder Name
# - Drivers License Number
# - Digital Signature
# - Credit Card Number
# - Security Code

from django.db import models
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField, PhoneNumberField

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from autoslug import AutoSlugField
from modeltools import Enum, format_filename as _ff, FilteredManager

Gender = Enum(
    ('MALE', 'M', 'Male'),
    ('FEMALE', 'F', 'Femail'),
)

CardType = Enum(
    ('MASTER', 'M', 'Master'),
    ('VISA', 'V', 'Visa'),
)



class Customer(models.Model):
    user = models.OneToOneField(User, null=True)
    gender = models.CharField(max_length=1, choices=Gender.choices())
    phone = PhoneNumberField(null=True,)
    birthday = models.DateField(null=True)
    
    def __unicode__(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)

    def get_card(self):    
        return Card.objects.get(customer=self.id)
        
class Address(models.Model):
    customer = models.OneToOneField(Customer)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = USStateField()
    zip_code = models.CharField(max_length=10)

    def __unicode__(self):
        return u'%s, %s, %s %s' % (self.street, self.city, self.state, self.zip_code)


class Card(models.Model):
    customer = models.OneToOneField(Customer)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=25)
    number = models.CharField(_('Card number'), max_length=16)
    type = models.CharField(max_length=2, choices=CardType.choices())
    security_code = models.CharField(max_length=255)
    expiry_date = models.DateField()

    class Meta():
        unique_together = ('customer', 'number')

    def __unicode__(self):
        return u'%s, %s' % (self.customer, self.number)
