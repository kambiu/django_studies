from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class MyUserInline(admin.StackedInline):
    model = models.MyUser
    can_delete = False
    verbose_name_plural = 'myuser'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (MyUserInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
admin.site.register(models.Group)
admin.site.register(models.Account)