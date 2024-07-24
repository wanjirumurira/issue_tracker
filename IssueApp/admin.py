from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

"""
We also need to register our custom user model with the admin
Tell the admin to use these forms by subclassing UserAdmin.

"""


admin.site.register(Project)
admin.site.register(CreateIssue)

