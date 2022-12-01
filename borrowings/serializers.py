import stripe
from django.db import transaction
from rest_framework import serializers

from borrowings.models import Borrowing
from borrowings.notification.bot import send_message, create_message
from payments.models import Payment


def borrowing_pay_session(book, money_to_pay):
    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": book.title,
                    },
                    "unit_amount": int(money_to_pay * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://127.0.0.1:8000/api/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://127.0.0.1:8000/api/cancel",
    )
    return session.id, session.url


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs["book"].inventory == 0:
            raise serializers.ValidationError("The book is not available")
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data.pop("book")

            book.inventory -= 1
            book.save()

            validated_data["book"] = book

            borrowing = Borrowing.objects.create(**validated_data)

            message = create_message(
                borrowing.expected_return_date,
                borrowing.book.title,
                borrowing.user,
            )
            send_message(message)

            money_to_pay = borrowing.expected_price
            session_id, session_url = borrowing_pay_session(book, money_to_pay)
            Payment.objects.create(
                status="PENDING",
                type="PAYMENT",
                borrowing=borrowing,
                session_url=session_url,
                session_id=session_id,
                money_to_pay=money_to_pay,
            )
        return borrowing

    class Meta:
        model = Borrowing
        fields = ("book", "expected_return_date")


class BorrowingListSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="title"
    )
    author = serializers.CharField(source="book.author", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "author",
            "user",
        )


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="title"
    )
    user = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="email"
    )

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )


class BorrowingReturnSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="title"
    )
    user = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="email"
    )

    class Meta:
        model = Borrowing
        fields = (
            "user",
            "book",
            "borrow_date",
            "actual_return_date",
        )
        read_only_fields = (
            "user",
            "book",
            "borrow_date",
            "actual_return_date",
        )
