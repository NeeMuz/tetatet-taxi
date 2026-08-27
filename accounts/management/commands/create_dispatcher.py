from django.core.management.base import BaseCommand

from accounts.models import User


class Command(BaseCommand):
    help = 'Создать или включить аккаунт диспетчера'

    def add_arguments(self, parser):
        parser.add_argument('--email', required=True, help='Email диспетчера')
        parser.add_argument('--password', required=True, help='Пароль')
        parser.add_argument('--first-name', default='Dispatcher', help='Имя')
        parser.add_argument('--last-name', default='', help='Фамилия')

    def handle(self, *args, **options):
        email = options['email'].strip()
        password = options['password']

        user = User.objects.filter(email__iexact=email).first()
        if user is None:
            user = User.objects.filter(username__iexact=email).first()

        if user is not None:
            user.is_dispatcher = True
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(
                f'Доступ диспетчера включён: {user.email} (логин: {user.username})'
            ))
            self.stdout.write('Вход: http://127.0.0.1:8000/dispatcher/login/')
            return

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=options['first_name'],
            last_name=options['last_name'],
            is_dispatcher=True,
        )
        self.stdout.write(self.style.SUCCESS(f'Диспетчер создан: {email}'))
        self.stdout.write('Вход: http://127.0.0.1:8000/dispatcher/login/')
