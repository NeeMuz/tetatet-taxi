# Generated manually

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_options_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=32, verbose_name='Телефон'),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=accounts.models.avatar_upload_path,
                verbose_name='Фото профиля',
            ),
        ),
    ]
