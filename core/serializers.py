from rest_framework import serializers
from .models import Restaurant, MenuItem, Order, OrderItem, Review

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'is_available']

class RestaurantSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone', 'longitude', 'latitude', 'menu_items']

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source='menu_item', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_id', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'restaurant', 'status', 'total', 'created_at', 'items']
        read_only_fields = ['status', 'total', 'created_at', 'user']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data['user'] = self.context['request'].user
        order = Order.objects.create(**validated_data)
        total = 0
        for item in items_data:
            price = item['menu_item'].price
            quantity = item['quantity']
            total += price * quantity
            OrderItem.objects.create(order=order, menu_item=item['menu_item'],
                                     quantity=quantity, price=price)
        order.total = total
        order.save()
        return order

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'order', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']
