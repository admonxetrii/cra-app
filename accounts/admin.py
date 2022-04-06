from django.contrib import admin
from .models import CustomUser, UserRestaurant
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('last_name', 'is_active', 'is_staff', 'is_superuser')
    ordering = ('-date_joined',)
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_verified')

    fieldsets = (
        (None, {
            'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'phone_number'
            )
        }),
        ('Permissions', {
            'fields': (
                'otp',
                'is_active',
                'is_staff',
                'is_superuser',
                'is_restaurant_representative',
                'is_customer',
            )
        }),
        ('Personal', {
            'fields': (
                'street',
                'city',
                'state',
                'profile_picture',
                'about',
                'userTags'
            )
        })
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'phone_number'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'is_restaurant_representative',
                'is_customer',
            )
        }),
        ('Personal', {
            'fields': (
                'street',
                'city',
                'state',
                'profile_picture',
                'about',
                'userTags'
            )
        })
    )


admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(UserRestaurant)
