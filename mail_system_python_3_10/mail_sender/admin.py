from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Mailing, MailingUser

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_subscribed', 'is_staff',)
    search_fields = ('email', 'username',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'is_subscribed')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


class MailingUserInline(admin.TabularInline):
    model = MailingUser


class MailingAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    inlines = (MailingUserInline,)


class MailingUserAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'user', 'is_seen',)
    list_filter = ('is_seen', 'mailing')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Mailing, MailingAdmin)
admin.site.register(MailingUser, MailingUserAdmin)
