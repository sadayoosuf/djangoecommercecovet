from django.contrib import admin
from cart.models import Cart,order_details,Payment


admin.site.register(Cart)
admin.site.register(order_details)
admin.site.register(Payment)
