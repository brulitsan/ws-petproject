from django.contrib import admin
from .models import User, UserProfile, UserProduct

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(UserProduct)