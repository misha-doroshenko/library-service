from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from books.models import Book
from books.serializers import BookSerializer


class BookViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = ()
