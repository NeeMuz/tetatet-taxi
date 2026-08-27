from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_avatar_alter_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_dispatcher',
            field=models.BooleanField(
                default=False,
                help_text='Доступ к панели диспетчера',
                verbose_name='Диспетчер',
            ),
        ),
    ]
