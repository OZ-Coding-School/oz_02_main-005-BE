from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Member

class MemberAdmin(BaseUserAdmin):
    ordering = ['account']
    list_display = ['account', 'member_email', 'display_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('account', 'password')}),
        (_('Personal info'), {'fields': ('member_email', 'display_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff')}),
        (_('Important dates'), {'fields': ('last_login', 'created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('account', 'member_email', 'display_name', 'password1', 'password2'),
        }),
    )

    filter_horizontal = ()

admin.site.register(Member, MemberAdmin)
