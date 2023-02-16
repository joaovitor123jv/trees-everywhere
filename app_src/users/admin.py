from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Account, Profile, User
from .forms import CustomUserChangeForm, CustomUserCreatingForm


class UserAccountInline(admin.TabularInline):
    model = User.accounts.through
    extra = 0
    readonly_fields = ['created_at']


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    add_form = CustomUserCreatingForm
    form = CustomUserChangeForm
    model = User
    list_display = ['username', 'email', 'full_name', 'is_staff']
    readonly_fields = ['last_login', 'date_joined', 'is_superuser']
    # filter_horizontal = ['groups', 'user_permissions', 'accounts']
    inlines = [UserAccountInline]

    def full_name(self, obj):
        return obj.get_full_name()


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
