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
    phone = PhoneNumberField(null=True,)
    street = models.CharField(max_length=255)
    city = models.CharField(blank=True, max_length=255)
    state = USStateField(blank=True)
    zip_code = models.CharField(max_length=10)
    
    def __unicode__(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)
