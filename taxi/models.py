from django.conf import settings
from django.db import models

from .tariffs import TARIFF_CHOICES


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('accepted', 'Водитель едет'),
        ('arrived', 'На месте'),
        ('on_way', 'В пути'),
        ('done', 'Завершён'),
        ('cancelled', 'Отменён'),
    ]

    PAYMENT_TYPE_CHOICES = [
        ('cash', 'Наличные'),
        ('card', 'Карта'),
    ]

    TARIFF_CHOICES = TARIFF_CHOICES

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='Пользователь',
    )
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=32, verbose_name='Телефон')
    from_address = models.CharField(max_length=255, verbose_name='Откуда')
    to_address = models.CharField(max_length=255, verbose_name='Куда')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    driver_note = models.TextField(blank=True, verbose_name='Заметка диспетчера')
    driver_name = models.CharField(max_length=100, blank=True, verbose_name='Водитель')
    tariff = models.CharField(
        max_length=20,
        choices=TARIFF_CHOICES,
        default='economy',
        verbose_name='Тариф',
    )
    distance_km = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Расстояние (км)',
    )
    estimated_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name='Ориентировочная цена',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус',
    )
    payment_type = models.CharField(
        max_length=10,
        choices=PAYMENT_TYPE_CHOICES,
        default='cash',
        verbose_name='Оплата',
    )
    payment_card = models.ForeignKey(
        'accounts.PaymentCard',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='Карта оплаты',
    )
    trip_rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Оценка поездки',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлён')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"#{self.pk} {self.name} — {self.get_status_display()}"
