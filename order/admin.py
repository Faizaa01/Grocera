from django.contrib import admin
from order.models import Order, OrderItem, Cart, CartItem, Wishlist


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Wishlist)
