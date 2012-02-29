from django.contrib import admin

from .models import *

class CustomerAdmin(admin.ModelAdmin):
    model = Customer

admin.site.register(Address)
admin.site.register(Card)
admin.site.register(Customer, CustomerAdmin)

