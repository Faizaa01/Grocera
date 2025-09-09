from decimal import Decimal
from rest_framework import serializers
from django.contrib.auth import get_user_model
from product.models import Category, Product, Review, ProductImage



class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True, help_text="Return total number of products in the category")
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'product_count']




class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(
        method_name='get_current_user_name')

    class Meta:
        model = get_user_model()
        fields = ['id', 'name']

    def get_current_user_name(self, obj):
        return obj.get_full_name()        


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'ratings', 'comment']
        read_only_fields = ['user', 'product']

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    seller = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name','description', 'images','price','stock','category','reviews', 'seller']

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Price can not be negative')
        return price
