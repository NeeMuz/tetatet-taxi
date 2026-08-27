from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_user_passenger_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentcard',
            name='pan',
            field=models.CharField(blank=True, default='', max_length=19, verbose_name='Номер карты'),
        ),
    ]
