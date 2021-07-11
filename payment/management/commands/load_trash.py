from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from payment.models import PaymentAccount


class Command(BaseCommand):
    help = 'Load trash to DB'

    def handle(self, *args, **options):
        print('Start loading trash')

        try:
            User.objects.get(username='admin')
        except User.DoesNotExist:
            User.objects.create_superuser(username='admin', email='', password='admin')

        accounts = {
            'Петров Иван Сергеевич': {
                'balance': '1700',
                'hold': '300',
                'status': True
            },
            'Kazitsky Jason': {
                'balance': '200',
                'hold': '200',
                'status': True
            },
            'Пархоменко Антон Александрович': {
                'balance': '1000',
                'hold': '300',
                'status': True
            },
            'Петечкин Петр Измаилович': {
                'balance': '1000000',
                'hold': '1',
                'status': False
            }
        }
        for initials, data in accounts.items():
            PaymentAccount.objects.get_or_create(initials=initials, balance=data.get('balance'), hold=data.get('hold'),
                                                 status=data.get('status'))

        print('End loading trash')
