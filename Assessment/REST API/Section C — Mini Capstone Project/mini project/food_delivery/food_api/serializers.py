from rest_framework import serializers
from food_api.models import Category, MenuItem, Order


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        error_messages={
            'blank': 'Category name cannot be empty.',
            'required': 'Category name cannot be empty.'
        }
    )

    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Category name cannot be empty.")
        return value


class MenuItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        error_messages={
            'blank': 'Menu item name cannot be empty.',
            'required': 'Menu item name cannot be empty.'
        }
    )

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'category', 'is_available']

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Menu item name cannot be empty.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.username')
    item = serializers.CharField(
        error_messages={
            'blank': 'Item name cannot be empty.',
            'required': 'Item name cannot be empty.'
        }
    )

    class Meta:
        model = Order
        fields = ['id', 'customer', 'item', 'quantity', 'status', 'created_at']
        read_only_fields = ['customer', 'created_at']

    def validate_item(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Item name cannot be empty.")
        return value

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value

    def validate_status(self, value):
        valid_statuses = ['pending', 'confirmed', 'delivered']
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Status must be one of: {', '.join(valid_statuses)}"
            )
        return value
