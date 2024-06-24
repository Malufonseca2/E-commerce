from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User


# Register the model on the admin section thing
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "shipping_address",
              "amount_paid", "date_ordered", "status", "date_shipped", "refund_granted", "refund_requested"]
    inlines = [OrderItemInline]


admin.site.unregister(Order)


admin.site.register(Order, OrderAdmin)
