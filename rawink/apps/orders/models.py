import datetime
import decimal
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
import random

from modeltools import Enum, format_filename as _ff, FilteredManager
from django.contrib.localflavor.us.models import USStateField, PhoneNumberField

from rawink.apps.artists.models import ArtistWorkPhoto
from django.core.urlresolvers import reverse

StatusChoices = Enum(
    ('checkout','checkout', 'Undergoing checkout'),
    ('payment-pending', 'payment-pending', 'Waiting for payment'),
    ('payment-complete','payment-complete', 'Paid'),
    ('payment-failed','payment-failed', 'Payment failed'),
    ('started', 'started', 'Started'),
    ('finished', 'finished', 'Finished'),
    ('cancelled', 'cancelled', 'Cancelled'),
)

class Order(models.Model):
    """
    Add this to your concrete model:
    cart = models.ForeignKey(Cart, related_name='orders')
    """
    product = models.ForeignKey(ArtistWorkPhoto)
    status = models.CharField(_('order status'), max_length=32,
                              choices=StatusChoices.choices(), default='checkout')
    created = models.DateTimeField(default=datetime.datetime.now,
                                   editable=False, blank=True)
    last_status_change = models.DateTimeField(default=datetime.datetime.now,
                                   editable=False, blank=True)
    user = models.ForeignKey(User, blank=True, null=True, related_name='orders')

    billing_first_name = models.CharField(_("first name"),
                                          max_length=256, blank=True)
    billing_last_name = models.CharField(_("last name"),
                                         max_length=256, blank=True)
    billing_street_address_1 = models.CharField(_("street address 1"),
                                                max_length=256, blank=True)
    billing_street_address_2 = models.CharField(_("street address 2"),
                                                max_length=256, blank=True)
    billing_state = USStateField()
    
    billing_postal_code = models.CharField(_("postal code"),
                                           max_length=20, blank=True)
    billing_phone = PhoneNumberField(null=True,)
    
    payment_type = models.CharField(max_length=256, blank=True)
    payment_type_name = models.CharField(_('name'), max_length=128, blank=True,
                                         editable=False)
    payment_card =  models.CharField(_('Card number'), max_length=16)
    payment_price = models.DecimalField(_('unit price'), max_digits=12,
                                        decimal_places=4, default=0,
                                        editable=False)
    token = models.CharField(max_length=32, blank=True, default='')

    class Meta:
        # Use described string to resolve ambiguity of the word 'order' in English.
        verbose_name = _('order (business)')
        verbose_name_plural = _('orders (business)')
        ordering = ('-last_status_change',)

    def get_absolute_url(self):
        return reverse('order-detail', kwargs=dict(token=self.token))    
            
    def __unicode__(self):
        return "%s %s" % (self.product, self.last_status_change)    