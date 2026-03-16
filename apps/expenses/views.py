from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters

from .models import Expense
from .serializers import ExpenseSerializer, ExpenseListSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["category", "date"]
    ordering_fields = ["date", "amount", "created"]

    def get_queryset(self):
        return Expense.objects.filter(
            user=self.request.user
        ).select_related("category")

    def get_serializer_class(self):
        if self.action == "list":
            return ExpenseListSerializer
        return ExpenseSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)