from django.contrib import admin

from .models import User, UserProduct, UserProfile

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(UserProduct)
