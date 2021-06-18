from rest_framework import serializers, status
from .models import Feedback, Refer_Earn_Customer, Refer_Earn_Vendor, KitchenRequest
from django.contrib.auth import get_user_model

User = get_user_model()


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class Customer_Refer_EarnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refer_Earn_Customer
        fields = "__all__"


class Vendor_Refer_EarnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refer_Earn_Vendor
        fields = "__all__"


class KitchenRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenRequest
        fields = "__all__"