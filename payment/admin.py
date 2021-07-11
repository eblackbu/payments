from django.contrib import admin

# Register your models here.
from payment.models import PaymentAccount


@admin.register(PaymentAccount)
class PaymentAccountAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid', )
