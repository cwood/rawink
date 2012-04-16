import datetime
import decimal
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
import random

from modeltools import Enum, format_filename as _ff, FilteredManager
from django.contrib.localflavor.us.models import USStateField, PhoneNumberField

from rawink.apps.artists.models import ArtistWorkPhoto
from rawink.apps.customers.models import Customer

from django.core.urlresolvers import reverse

StatusChoices = Enum(
    ('checkout','checkout', 'Undergoing checkout'),
    ('payment-pending', 'payment-pending', 'Waiting for payment'),
    ('payment-complete','payment-complete', 'Paid'),
    ('payment-failed','payment-failed', 'Payment failed'),
    ('in_progress', 'in_progress', 'in-progress'),
    ('finished', 'finished', 'Finished'),
    ('confirmed', 'confirmed', 'Confirmed'),
    ('cancelled', 'cancelled', 'Cancelled'),
    ('pending', 'pending', 'Pending'),
    
)

class OrderManager(models.Manager):
    pass
    # def get_query_set(self):
    #     return super(ProductManager, self).get_query_set().filter(is_enabled=True)

BOOL_CHOICES = ((True, 'Hourly Rate'), (False, 'Fixed Rate'))
class Order(models.Model):
    """
    Add this to your concrete model:
    cart = models.ForeignKey(Cart, related_name='orders')
    """
    product = models.ForeignKey(ArtistWorkPhoto)
    customer = models.ForeignKey(Customer)
    
    status = models.CharField(_('order status'), max_length=32,
                              choices=StatusChoices.choices(), default='pending')
    created = models.DateTimeField(default=datetime.datetime.now,
                                   editable=False, blank=True)
    last_status_change = models.DateTimeField(default=datetime.datetime.now,
                                   editable=False, blank=True)
    
    payment_type = models.BooleanField(choices=BOOL_CHOICES)
    payment_price = models.DecimalField(_('Total price'), max_digits=12,
                                        decimal_places=4, default=0)
    token = models.CharField(max_length=6, blank=True, default='')
    
    
    objects = OrderManager()
    started = FilteredManager(status='started')
    
    def save(self, *args, **kwargs):
        if not self.token:
            for i in xrange(100):
                token = ''.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyz', 6))
                if not type(self).objects.filter(token=token).exists():
                    self.token = token
                    break
        return super(Order, self).save(*args, **kwargs)

    class Meta:
        # Use described string to resolve ambiguity of the word 'order' in English.
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ('-last_status_change',)

    def get_absolute_url(self):
        return reverse('order-detail', kwargs=dict(pk=self.id))
            
    def __unicode__(self):
        return "%s %s" % (self.product, self.last_status_change)    