from rest_framework import serializers
from apps.categories.serializer import CategorySerializer
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=__import__("apps.categories.models", fromlist=["Category"]).Category.objects.all(),
        write_only=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Expense
        fields = [
            "id",
            "category",
            "category_id",
            "amount",
            "date",
            "note",
            "created",
            "updated",
        ]
        read_only_fields = ["id", "created", "updated"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value


class ExpenseListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Expense
        fields = ["id", "category_name", "amount", "date", "note"]