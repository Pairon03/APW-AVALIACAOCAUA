from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404

# Produtos 
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny] 

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

# Carrinho de Compras
class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        product = get_object_or_404(Product, id=product_id)

        order, created = Order.objects.get_or_create(user=user, status='PROCESSING', defaults={'total': 0, 'discount': 0, 'payment_method':'PIX'})

        item, created_item = OrderItem.objects.get_or_create(order=order, product=product, defaults={'quantity': quantity, 'price': product.price})
        if not created_item:
            item.quantity += int(quantity)
            item.save()

        order.total = sum([i.price*i.quantity for i in order.items.all()]) - order.discount
        order.save()

        return Response({'message': 'Produto adicionado ao carrinho', 'order_id': order.id})


# Status do pedido 
class UpdateOrderStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        user = request.user
        new_status = request.data.get('status')
        order = get_object_or_404(Order, id=order_id)


        group_names = [g.name for g in user.groups.all()]
        allowed = False

        if new_status in ['PAID', 'PAYMENT_FAILED', 'INVOICE'] and 'FINANCEIRO' in group_names:
            allowed = True
        elif new_status in ['PREPARING', 'SENT'] and 'LOGISTICA' in group_names:
            allowed = True
        elif new_status in ['RECEIVED', 'RETURN_REQUEST'] and 'CLIENTE' in group_names:
            allowed = True
        elif new_status in ['RETURNING', 'RETURNED', 'RETURN_CANCELED'] and 'POS_VENDA' in group_names:
            allowed = True

        if not allowed:
            return Response({'error': 'Você não tem permissão para alterar esse status'}, status=status.HTTP_403_FORBIDDEN)

        order.status = new_status
        order.save()
        return Response({'message': f'Status do pedido atualizado para {new_status}'})
    
# Avaliação de produto 
class ProductReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        order_item_id = request.data.get('order_item_id')
        rating = int(request.data.get('rating'))
        comment = request.data.get('comment', '')

 
        if rating < 1 or rating > 5:
            return Response({'error': 'A nota deve ser entre 1 e 5'}, status=status.HTTP_400_BAD_REQUEST)

        order_item = get_object_or_404(OrderItem, id=order_item_id)
        if order_item.order.user != user:
            return Response({'error': 'Você só pode avaliar produtos que comprou'}, status=status.HTTP_403_FORBIDDEN)

        product = get_object_or_404(Product, id=product_id)


        ProductReview.objects.create(user=user, product=product, order_item=order_item, rating=rating, comment=comment)


        reviews = ProductReview.objects.filter(product=product)
        product.total_reviews = reviews.count()
        product.average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
        product.save()

        return Response({'message': 'Avaliação registrada com sucesso'})

