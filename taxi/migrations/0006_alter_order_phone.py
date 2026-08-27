from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0005_order_driver_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=32, verbose_name='Телефон'),
        ),
    ]
