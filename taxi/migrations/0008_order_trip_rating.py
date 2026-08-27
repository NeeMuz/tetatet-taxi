from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_paymentcard'),
        ('taxi', '0007_order_payment_card_order_payment_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='trip_rating',
            field=models.PositiveSmallIntegerField(
                blank=True,
                null=True,
                verbose_name='Оценка поездки',
            ),
        ),
    ]
