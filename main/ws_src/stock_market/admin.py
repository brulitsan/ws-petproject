from django.contrib import admin

from .models import Order, Product, ProductCategories

admin.site.register(ProductCategories)
admin.site.register(Product)
admin.site.register(Order)
