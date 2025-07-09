import requests
from rest_framework import serializers

from .models import Cart, CartItem
from django.conf import settings

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ['id']

class CartSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']