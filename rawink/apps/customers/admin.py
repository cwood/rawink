from django.contrib import admin

from .models import *

class AddressInline(admin.StackedInline):
    model = Address

class CardInline(admin.StackedInline):
    model = Card
    
class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    
    inlines = [AddressInline, CardInline]

admin.site.register(Customer, CustomerAdmin)

