from django.contrib import admin
from .models import Item, CartItem, Cart, Payment, Coupon


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'ordered')

admin.site.register(Item)
admin.site.register(CartItem)
admin.site.register(Cart, CartAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
