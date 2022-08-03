from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """ Custom User Admin"""

    fieldsets = UserAdmin.fieldsets + \
        (("Custom Profile", {"fields": ('login_method', "email_verified", "office","tel", "bio", "avatar")}),)
    list_display = ("username", "email", "login_method", "email_verified", "office","tel", "created", "get_avatar")

    def get_avatar(self, obj):
        try:
            return mark_safe(f'<img width="18px" src="{obj.avatar.url}" />')
        except:
            pass
    get_avatar.short_description = "Profile Image"
