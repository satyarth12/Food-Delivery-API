from rest_framework import serializers, status
from .models import Order, OrderHistory
from django.contrib.auth import get_user_model

User = get_user_model()


class OrderSerializer(serializers.ModelSerializer):
    order_status = serializers.SerializerMethodField()
    out_for_delivery = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()
    order_placed_at = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'item_names', 'total_items', 'order_total', 'user', 'kitchen_name',
                'order_date', 'order_slot_from', 'order_slot_to', 'order_placed',
                'order_placed_at', 'order_status', 'out_for_delivery', 'completed')

    def get_order_status(self, obj):
        if obj.order_placed == True:
            order_hist = OrderHistory.objects.get(order = obj)
            if order_hist:
                return order_hist.order_status
        return 'Order not placed'

    def get_out_for_delivery(self, obj):
        if obj.order_placed == True:
            order_hist = OrderHistory.objects.get(order = obj)
            if order_hist:
                return order_hist.delivery
        return 'Order not placed'

    def get_completed(self, obj):
        if obj.order_placed == True:
            order_hist = OrderHistory.objects.get(order = obj)
            if order_hist:
                return order_hist.complete
        return 'Order not placed'

    def get_order_placed_at(self, obj):
        if obj.order_placed == True:
            order_hist = OrderHistory.objects.get(order = obj)
            if order_hist:
                return order_hist.created_at
        return 'Order not placed'



class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = '__all__'

