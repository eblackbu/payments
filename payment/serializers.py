from rest_framework import serializers

from payment.models import PaymentAccount


class PaymentAccountReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentAccount
        fields = '__all__'


class AccountOperationSerializer(serializers.Serializer):
    id = serializers.CharField(min_length=36, max_length=36)
    amount = serializers.CharField(max_length=10)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
