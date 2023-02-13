from django.contrib import admin

from .models import Account, Profile


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'active']
    search_fields = ['name']
    readonly_fields = ['created']
    list_filter = ['active']
    list_editable = ['active']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['joined', 'text']
    search_fields = ['text', 'joined']
    readonly_fields = ['joined']
    list_filter = ['joined']
