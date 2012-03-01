from django.contrib import admin

from .models import *



class OrderAdmin(admin.ModelAdmin):
    model = Order
    # prepopulated_fields = {'slug': ("user.first_name", "user.last_name")}

admin.site.register(Order, OrderAdmin)

