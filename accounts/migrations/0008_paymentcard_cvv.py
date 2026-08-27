from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_paymentcard_pan'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentcard',
            name='cvv',
            field=models.CharField(blank=True, default='', max_length=4, verbose_name='CVV'),
        ),
    ]
