from django.contrib import admin
from .models import ProductCategories, Product, Order

admin.site.register(ProductCategories)
admin.site.register(Product)
admin.site.register(Order)