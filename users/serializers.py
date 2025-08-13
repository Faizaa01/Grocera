from users.models import Deposit
from rest_framework import serializers
from order.serializers import WishlistSerializer, OrderSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'password', 'first_name','last_name', 'address', 'phone_number']


class UserSerializer(BaseUserSerializer):
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    wishlist_items = WishlistSerializer(many=True, read_only=True)
    orders = OrderSerializer(many=True, read_only=True)

    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fields = ['id', 'email', 'first_name', 'last_name', 'address', 'phone_number', 'balance','wishlist_items', 'orders']
        

class DepositSerializer(serializers.ModelSerializer):
    updated_balance = serializers.SerializerMethodField()
    class Meta:
        model = Deposit
        fields = ['id', 'user', 'amount', 'status', 'transaction_reference', 'created_at', 'updated_at','updated_balance']
        read_only_fields = ['status', 'created_at', 'transaction_reference', 'updated_at', 'user','updated_balance']

    def create(self, validated_data):
        user = self.context['request'].user
        deposit = Deposit.objects.create(user=user, amount=validated_data['amount'], status='completed')
        user.balance += validated_data['amount']
        user.save()
        return deposit
    
    def get_updated_balance(self, obj):
        return obj.user.balance
    
    def get_fields(self):
        fields = super().get_fields()
        if self.instance is not None:
            fields['amount'].read_only = True
        return fields
    