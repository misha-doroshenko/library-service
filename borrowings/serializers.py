import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from borrowings.models import Borrowing


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
    actual_return_date = serializers.DateField()

    class Meta:
        model = Borrowing
        fields = ("actual_return_date",)

    def validate(self, attrs):
        if attrs["actual_return_date"] < datetime.date.today():
            raise ValidationError("U can't go back in time" " date is wrong!")
        return super(BorrowingReturnSerializer, self).validate(attrs)
