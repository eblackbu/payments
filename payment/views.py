from decimal import Decimal

from django.core.exceptions import ValidationError

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from payment.models import PaymentAccount
from payment.serializers import PaymentAccountReadSerializer, AccountOperationSerializer


class PaymentAccountViewSet(viewsets.GenericViewSet):
    queryset = PaymentAccount.objects.all()
    serializer_mapping = {
        'add': AccountOperationSerializer,
        'substract': AccountOperationSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_mapping.get(self.action, PaymentAccountReadSerializer)

    @staticmethod
    def _get_account(uuid):
        if not uuid:
            raise ValidationError('Не был передан параметр id')
        try:
            account = PaymentAccount.objects.get(uuid=uuid)
        except PaymentAccount.DoesNotExist:
            raise ValidationError('Не существует аккаунта с указанным id')
        return account

    @action(detail=False, methods=['get'])
    def ping(self, request):
        # debug_task.delay()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def add(self, request):
        """
        Вычитает в параметре холда сумму, переданную в параметре amount.
        request.data = {
            'id': uuid
            'amount': string, содержащий точный decimal с двумя знаками после запятой
        }
        """
        try:
            account = self._get_account(request.data.get('id'))
        except ValidationError as e:
            return Response({
                'status': 400,
                'result': False,
                'addition': {},
                'description': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = Decimal(request.data.get('amount'))
            if amount <= 0:
                raise ValueError
        except ValueError:
            return Response({
                'status': 400,
                'result': False,
                'addition': {},
                'description': 'Передано некорректное значение amount'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not account.status:
            return Response({
                'status': 200,
                'result': False,
                'addition': PaymentAccountReadSerializer(account).data,
                'description': 'Данный счет заблокирован для проведения операций'
            }, status=status.HTTP_200_OK)

        account.hold -= amount
        account.save()

        return Response({
            'status': 200,
            'result': True,
            'addition': PaymentAccountReadSerializer(account).data,
            'description': f'Операция выполнена успешно'
        })

    @action(detail=False, methods=['post'])
    def substract(self, request):
        """
        Прибавляет к параметру холда сумму, переданную в параметре amount.
        При недостатке средств на счете возвращает HTTP 400
        request.data = {
            'id': uuid
            'amount': string, содержащий точный decimal с двумя знаками после запятой
        }
        """
        try:
            account = self._get_account(request.data.get('id'))
        except ValidationError as e:
            return Response({
                'status': 400,
                'result': False,
                'addition': {},
                'description': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = Decimal(request.data.get('amount'))
            if amount <= 0:
                raise ValueError
        except ValueError:
            return Response({
                'status': 400,
                'result': False,
                'addition': PaymentAccountReadSerializer(account).data,
                'description': 'Передано некорректное значение amount'
            }, status=status.HTTP_400_BAD_REQUEST)

        if account.balance - account.hold - amount < 0:
            return Response({
                'status': 200,
                'result': False,
                'addition': PaymentAccountReadSerializer(account).data,
                'description': 'На счете недостаточно денег для проведения операции'
            }, status=status.HTTP_200_OK)

        if not account.status:
            return Response({
                'status': 200,
                'result': False,
                'addition': PaymentAccountReadSerializer(account).data,
                'description': 'Данный счет заблокирован для проведения операций'
            }, status=status.HTTP_200_OK)

        account.hold += amount
        account.save()

        return Response({
            'status': 200,
            'result': True,
            'addition': PaymentAccountReadSerializer(account).data,
            'description': f'Операция выполнена успешно'
        })

    @action(detail=False, methods=['get'])
    def status(self, request):
        """
        Получить статус по uuid, переданному в GET-параметре
        request.data = {
            'id': uuid
        }
        """
        try:
            account = self._get_account(request.query_params.get('id'))
        except ValidationError as e:
            return Response({
                'status': 400,
                'result': False,
                'addition': {},
                'description': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'status': 200,
            'result': True,
            'addition': PaymentAccountReadSerializer(account).data,
            'description': f'Остаток по балансу {str(account.balance)}, статус {"Открыт" if account.status else "Закрыт"}'
        })
