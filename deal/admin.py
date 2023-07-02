from django.contrib import admin

from .models import Customer, Order


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
