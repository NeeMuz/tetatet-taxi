from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('accepted', 'Принят'),
        ('on_way', 'В пути'),
        ('done', 'Завершён'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    from_address = models.CharField(max_length=255)
    to_address = models.CharField(max_length=255)
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} — {self.get_status_display()}"
