from django.contrib import admin

from .models import Cart, CartItem, OrderItem, Order


class CartAdmin(admin.ModelAdmin):
    pass


class CartItemAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date_created', 'total_price')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'from_date', 'to_date', 'price', 'date_created', 'status')

    def date_created(self, obj):
        return obj.order.date_created

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
