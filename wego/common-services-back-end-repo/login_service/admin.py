from django.contrib import admin
from .models import BaseUser
# Register your models here.
class BaseUserAdmin(admin.ModelAdmin):
    model = BaseUser
    list_display = ['email', 'username', 'password', 'is_active']
admin.site.register(BaseUser, BaseUserAdmin)
