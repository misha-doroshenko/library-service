import datetime

from django.db import transaction
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer,
    borrowing_pay_session,
)
from payments.models import Payment


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.select_related("book", "user")
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Borrowing.objects.select_related("book", "user")

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if is_active:
            queryset = queryset.filter(actual_return_date=None)

        if self.request.user.is_staff and user_id:
            queryset = queryset.filter(user_id=int(user_id))

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        if self.action == "create":
            return BorrowingCreateSerializer

        if self.action == "return_book":
            return BorrowingReturnSerializer

        return BorrowingSerializer

    def get_permissions(self):
        if self.action in ("create", "update"):
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        methods=["POST"],
        detail=True,
        url_path="return-book",
        permission_classes=[IsAuthenticated],
    )
    def return_book(self, request, pk=None):
        """endpoint for return borrowed book"""
        borrowing = get_object_or_404(Borrowing, pk=pk)
        book = borrowing.book

        serializer = self.get_serializer(borrowing, data=self.request.data)

        if not borrowing.actual_return_date and serializer.is_valid():
            book.inventory += 1
            borrowing.actual_return_date = datetime.date.today()
            book.save()
            borrowing.save()
            if borrowing.overdue:
                with transaction.atomic():
                    session_id, session_url = borrowing_pay_session(
                        book, borrowing.overdue
                    )
                    Payment.objects.create(
                        status="PENDING",
                        type="FINE",
                        borrowing=borrowing,
                        session_url=session_url,
                        session_id=session_id,
                        money_to_pay=borrowing.overdue,
                    )

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "is_active",
                type=str,
                description="Filter by borrowed book status (ex. ?is_active=None)",
            ),
            OpenApiParameter(
                "is_staff",
                type=int,
                description="Filter by user (ex. ?user_id=1)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
