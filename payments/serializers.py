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

    def create(self, validated_data):
        status = validated_data["status"]
        type = validated_data["type"]
        borrowing = validated_data["borrowing"]
        money_to_pay = borrowing.book.daily_fee * 7

        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": borrowing.book.title,
                        },
                        "unit_amount": int(money_to_pay * 100),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="http://localhost:4242/success",
            cancel_url="http://localhost:4242/cancel",
        )
        return Payment.objects.create(
            status=status,
            type=type,
            borrowing=borrowing,
            session_url=session.url,
            session_id=session.id,
            money_to_pay=money_to_pay,
        )


class PaymentDetailSerializer(PaymentSerializer):
    borrowing = BorrowingDetailSerializer()
