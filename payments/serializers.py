from rest_framework import serializers

from borrowings.serializers import BorrowingDetailSerializer
from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        )


class PaymentDetailSerializer(PaymentSerializer):
    borrowing = BorrowingDetailSerializer()
