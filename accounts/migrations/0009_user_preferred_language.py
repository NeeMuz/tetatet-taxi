from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_paymentcard_cvv'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='preferred_language',
            field=models.CharField(
                choices=[('ru', 'Русский'), ('uk', 'Українська'), ('en', 'English')],
                default='ru',
                max_length=5,
                verbose_name='Язык интерфейса',
            ),
        ),
    ]
