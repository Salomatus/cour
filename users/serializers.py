from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone",
            "avatar",
            "town",
            "is_superuser",
            "is_staff",
            "is_active",
        ]
