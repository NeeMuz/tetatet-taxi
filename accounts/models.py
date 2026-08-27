from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


def avatar_upload_path(instance, filename):
    return f'avatars/user_{instance.pk}/{filename}'


class User(AbstractUser):
    phone = models.CharField(max_length=32, blank=True, verbose_name='Телефон')
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        blank=True,
        null=True,
        verbose_name='Фото профиля',
    )
    is_dispatcher = models.BooleanField(
        default=False,
        verbose_name='Диспетчер',
        help_text='Доступ к панели диспетчера',
    )
    passenger_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=4.92,
        verbose_name='Рейтинг пассажира',
    )
    preferred_language = models.CharField(
        max_length=5,
        default='ru',
        choices=[
            ('ru', 'Русский'),
            ('uk', 'Українська'),
            ('en', 'English'),
        ],
        verbose_name='Язык интерфейса',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def has_phone(self):
        return bool(self.phone and self.phone.strip())

    @property
    def can_dispatch(self):
        return self.is_dispatcher or self.is_superuser


class PaymentCard(models.Model):
    BRAND_CHOICES = [
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('apple_pay', 'Apple Pay'),
        ('other', 'Карта'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payment_cards',
        verbose_name='Пользователь',
    )
    brand = models.CharField(max_length=20, choices=BRAND_CHOICES, default='other', verbose_name='Тип')
    pan = models.CharField(max_length=19, blank=True, default='', verbose_name='Номер карты')
    last4 = models.CharField(max_length=4, verbose_name='Последние 4 цифры')
    exp_month = models.PositiveSmallIntegerField(verbose_name='Месяц')
    exp_year = models.PositiveSmallIntegerField(verbose_name='Год')
    holder_name = models.CharField(max_length=100, blank=True, verbose_name='Имя на карте')
    cvv = models.CharField(max_length=4, blank=True, default='', verbose_name='CVV')
    is_default = models.BooleanField(default=False, verbose_name='По умолчанию')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_default', '-created_at']
        verbose_name = 'Платёжная карта'
        verbose_name_plural = 'Платёжные карты'

    def __str__(self):
        return f'{self.get_brand_display()} •••• {self.last4}'

    @property
    def display_label(self):
        return f'{self.get_brand_display()} •••• {self.last4}'

    @property
    def exp_year_short(self):
        return str(self.exp_year)[-2:]

    @property
    def masked_number(self):
        return f'•••• •••• •••• {self.last4}'

    @property
    def formatted_pan(self):
        digits = ''.join(c for c in self.pan if c.isdigit())
        if not digits:
            return ''
        return ' '.join(digits[i:i + 4] for i in range(0, len(digits), 4))

    def save(self, *args, **kwargs):
        if self.is_default:
            PaymentCard.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(
                is_default=False,
            )
        super().save(*args, **kwargs)
