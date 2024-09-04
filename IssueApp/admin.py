from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import *
"""
We also need to register our custom user model with the admin
Tell the admin to use these forms by subclassing UserAdmin.

"""

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('username', 'email', 'profile_image', 'occupation', 'is_staff','is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'profile_image', 'occupation')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'profile_image', 'occupation', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Project)
admin.site.register(CreateIssue)
admin.site.register(TeamInvitation)
