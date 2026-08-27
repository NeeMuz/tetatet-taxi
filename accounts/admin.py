from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import PaymentCard, User


@admin.register(PaymentCard)
class PaymentCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'brand', 'last4', 'exp_month', 'exp_year', 'is_default', 'created_at')
    list_filter = ('brand', 'is_default')
    search_fields = ('user__email', 'last4', 'holder_name')
    raw_id_fields = ('user',)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_dispatcher', 'is_staff', 'is_active')
    list_filter = ('is_dispatcher', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('email',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Tetatet', {'fields': ('phone', 'avatar', 'is_dispatcher')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Tetatet', {'fields': ('phone', 'avatar', 'is_dispatcher')}),
    )
