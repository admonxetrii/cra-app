from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class UserAdminConfig(UserAdmin):
    pass

admin.site.register(CustomUser, UserAdminConfig)