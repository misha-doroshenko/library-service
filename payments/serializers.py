from rest_framework import serializers

from borrowings.serializers import BorrowingDetailSerializer
from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"


class PaymentDetailSerializer(PaymentSerializer):
    borrowing = BorrowingDetailSerializer()
