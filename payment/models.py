import uuid as uuid
from django.db import models

# Create your models here.


class PaymentAccount(models.Model):

    class Meta:
        verbose_name = 'Счет абонента'
        verbose_name_plural = 'Счета абонентов'

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='Идентификатор')
    initials = models.CharField(max_length=200, verbose_name='ФИО')
    balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Баланс')
    hold = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Холд')
    status = models.BooleanField(default=True, verbose_name='Статус', null=False)

    def __str__(self):
        return f'Счет клиента {self.initials}'
