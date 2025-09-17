from rest_framework import serializers
from .models import *

# Produto 
class ProductPieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPiece
        fields = ['name', 'measurements', 'weight']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image_url', 'is_main']

class ProductSerializer(serializers.ModelSerializer):
    pieces = ProductPieceSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category_name',
                  'pieces', 'images', 'total_reviews', 'average_rating']
        
# Usuário 
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password', 'is_superuser', 'groups', 'user_permissions', 'last_login']

# Pedido 
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total', 'discount', 'payment_method',
                  'status', 'tracking_code', 'created_at', 'items']
        
# Avaliação
class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'product', 'order_item', 'rating', 'comment', 'created_at']

