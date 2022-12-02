import stripe
from django.conf import settings
from rest_framework import serializers

from borrowings.serializers import BorrowingDetailSerializer
from payments.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


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
        read_only_fields = (
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        )


class PaymentListSerializer(serializers.ModelSerializer):
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
        read_only_fields = ("session_url", "session_id", "money_to_pay")


class PaymentDetailSerializer(PaymentSerializer):
    borrowing = BorrowingDetailSerializer()
