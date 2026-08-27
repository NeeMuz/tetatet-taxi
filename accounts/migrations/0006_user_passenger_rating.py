from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_paymentcard'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='passenger_rating',
            field=models.DecimalField(
                decimal_places=2,
                default=4.92,
                max_digits=3,
                verbose_name='Рейтинг пассажира',
            ),
        ),
    ]
