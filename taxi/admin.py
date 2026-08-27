from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'phone',
        'route_short',
        'status',
        'tariff',
        'estimated_price',
        'user',
        'created_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone', 'from_address', 'to_address', 'comment', 'driver_note')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at', 'estimated_price')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Клиент', {
            'fields': ('user', 'name', 'phone'),
        }),
        ('Маршрут', {
            'fields': ('from_address', 'to_address', 'distance_km', 'tariff', 'comment', 'estimated_price'),
        }),
        ('Обработка', {
            'fields': ('status', 'driver_name', 'driver_note'),
        }),
        ('Система', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    actions = ['mark_accepted', 'mark_on_way', 'mark_done', 'mark_cancelled']

    def save_model(self, request, obj, form, change):
        if not obj.estimated_price:
            from .services import estimate_price
            obj.estimated_price = estimate_price(
                obj.from_address,
                obj.to_address,
                distance_km=obj.distance_km,
                tariff=obj.tariff or 'economy',
            )
        super().save_model(request, obj, form, change)

    @admin.display(description='Маршрут')
    def route_short(self, obj):
        return f'{obj.from_address[:30]} → {obj.to_address[:30]}'

    def _set_status(self, queryset, status):
        for order in queryset:
            order.status = status
            order.save()

    @admin.action(description='Принять выбранные заказы')
    def mark_accepted(self, request, queryset):
        self._set_status(queryset, 'accepted')

    @admin.action(description='Отметить «В пути»')
    def mark_on_way(self, request, queryset):
        self._set_status(queryset, 'on_way')

    @admin.action(description='Завершить выбранные заказы')
    def mark_done(self, request, queryset):
        self._set_status(queryset, 'done')

    @admin.action(description='Отменить выбранные заказы')
    def mark_cancelled(self, request, queryset):
        self._set_status(queryset, 'cancelled')
