from rest_framework import mixins, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from payments.models import Payment
from payments.serializers import (
    PaymentSerializer,
    PaymentDetailSerializer,
    PaymentListSerializer,
)


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    model = Payment
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = Payment.objects.select_related("borrowing")
        if self.request.user.is_staff:
            return queryset
        queryset = queryset.filter(borrowing__user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action in ["list", "create"]:
            return PaymentListSerializer
        if self.action in ("retrieve", "success"):
            return PaymentDetailSerializer
        return PaymentSerializer


@api_view(["GET"])
def success_payment(request, *args, **kwargs):
    session_id = request.query_params.get("session_id", "")
    if session_id:
        payment = Payment.objects.get(session_id=session_id)
        payment.status = "Paid"
        payment.save()
        serializer = PaymentDetailSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def cancel_payment(request):
    message = (
        "payment can be paid a bit later"
        "(but the session is available for only 24h)"
    )
    return Response(message, status=status.HTTP_200_OK)
